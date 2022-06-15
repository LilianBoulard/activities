"""
Gets data from opendata.paris.fr and stores them in the Redis database.
"""

import re
import requests

from functools import reduce
from datetime import datetime
from itertools import zip_longest
from dateutil.parser import isoparse
from pydantic import ValidationError
from typing import List, Optional, Generator, Iterable

from activities.config import timezone
from activities.database.redis import db, Event
from activities.utils import decode_json, price_regex


def batcher(iterable: Iterable, n: int):
    # Iterate a list in batches of size n.
    # From https://stackoverflow.com/a/34166690/9084059
    args = [iter(iterable)] * n
    return zip_longest(*args)


headers = {
    "Host": "opendata.paris.fr",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}


def get_event_from_row(row: dict) -> Optional[Event]:

    identifier = row.get('id', None)
    if not identifier:
        return

    title = row.get('title', None)
    if not title:
        return

    tags = row.get('tags', None)
    if not tags:
        return

    # Process reservation info
    reservation_required_val = row.get('access_type', None)
    if not reservation_required_val:
        return
    reservation_map = {
        'non': False,
        'conseillée': True,
        'obligatoire': True,
    }
    if reservation_required_val not in reservation_map.keys():
        print(f'Unknown access type: {reservation_required_val!r}')
        return
    reservation_required = reservation_map[reservation_required_val]

    reservation_url = row.get('access_link', '')
    if not reservation_url and reservation_required:
        return

    reservation_url_description = row.get('access_link_text', 'Billetterie')

    # Process `date_start`
    date_start_val = row.get('date_start', None)
    if not date_start_val:
        return
    date_start = isoparse(date_start_val)

    # Process occurrences (`date_end`)
    occurrences_val = row.get('occurrences', None)
    if not occurrences_val:
        return  # FIXME: Mandatory ?
    occurrences = occurrences_val.split(';')
    occurrences_start_end = [
        (start, end)
        for occ in occurrences
        for start, end in occ.split('_')
    ]
    occurrences_start: List[datetime] = [
        isoparse(occ[0]) for occ in occurrences_start_end
    ]
    # Get the last occurrence (date-wise), which will be our `date_end`
    date_end = reduce(lambda acc, occ: acc if acc > occ else occ, occurrences_start)

    # Process prices
    price_type = row.get('price_type', None)
    if not price_type:
        return
    price_detail = row.get('price_detail', None)
    if not price_detail:
        # TODO: Edge cases:
        #  - "Sur réservation"
        return
    if price_type == 'payant':
        found_prices = re.findall(price_regex, price_detail)

        # FIXME: Hackish
        all_prices = []
        for price_matches in found_prices:
            # Remove duplicates
            matches = list(set(price_matches))
            # Remove empty values
            matches.remove('')
            # Keep only the first integer value
            for match in matches:
                try:
                    price = int(match)
                    break
                except ValueError:
                    continue
            else:
                # If we did not find any integer value,
                # print a warning and skip this price
                print(f'Match did not contain any price: {matches}')
                continue
            all_prices.append(price)
    else:
        all_prices = [0]

    # Process geographic location
    place = row.get('address_name', None)
    if not place:
        return
    street = row.get('address_street', None)
    if not street:
        return
    city = row.get('address_city', None)
    if not city:
        return
    zipcode = row.get("address_zipcode", None)
    if not zipcode:
        return
    department = int(zipcode[:2])
    district = zipcode[-2:] if zipcode.startswith('75') else 0

    lat, lon = row.get('lat_lon', (None, None))
    if not lat or not lon:
        return

    try:
        event = Event(
            identifier=identifier,
            title=title,
            tags=tags,

            reservation_required=reservation_required,
            reservation_url=reservation_url,
            reservation_url_description=reservation_url_description,

            date_start=date_start,
            date_end=date_end,

            price_type=price_type,
            price_detail=price_detail,
            price_start=min(all_prices),
            price_end=max(all_prices),

            contact_url=row.get('contact_url', ''),
            contact_mail=row.get('contact_mail', ''),
            contact_phone=row.get('contact_phone', ''),
            contact_facebook=row.get('contact_facebook', ''),
            contact_twitter=row.get('contact_twitter', ''),

            place=place,
            street=street,
            city=city,
            zipcode=zipcode,
            department=department,
            district=district,

            latitude=lat,
            longiture=lon,

            blind=bool(row.get('blind', 0)),
            deaf=bool(row.get('deaf', 0)),
            pmr=bool(row.get('pmr', 0)),
        )
    except ValidationError:
        print('Invalid event')
    else:
        return event


def get_clean_events(records: list) -> Generator[Event, None, None]:
    for record in records:
        index: int

        event = get_event_from_row(record['fields'])
        if event is not None:
            yield event


def que_faire_a_paris() -> None:
    """
    Gets the "Que Faire à Paris ?" dataset and add it to the database.
    This data source is updated everyday, around 6-7 AM.
    If the database has already been downloaded today, it is read from disk.
    Source: https://opendata.paris.fr/explore/dataset/que-faire-a-paris-/
    """

    last_save = datetime.fromtimestamp(db.lastsave())
    now = datetime.now(timezone)
    last_update = datetime(year=now.year, month=now.month, day=now.day, hour=7)
    if last_save > last_update:
        print('Data was already saved earlier this day, skipping pull')
        return

    # Get all the event ids we got in the database
    db_record_ids = {}
    for key_batch in batcher(db.scan_iter('user:*'), 500):
        db_record_ids.update(key_batch)

    # Searches for the 10k first events, with the timezone set on Paris.
    endpoint = ("https://opendata.paris.fr/api/records/1.0/search/"
                "?dataset=que-faire-a-paris-&q="
                "&rows=10000"
                "&timezone=Europe%2FParis")

    with requests.get(endpoint, headers=headers) as r:
        data = decode_json(r.text)

    for record in data['records']:
        if int(record['fields']['id']) in db_record_ids:
            continue
        event = get_event_from_row(record['fields'])
        event.save()

    db.save()


if __name__ == "__main__":
    que_faire_a_paris()
