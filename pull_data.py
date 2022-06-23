"""
Gets data from opendata.paris.fr and stores them in the Redis database.
"""

import requests

from functools import reduce
from datetime import datetime
from redis_om import Migrator
from dateutil.parser import isoparse
from pydantic import ValidationError
from typing import List, Optional, Generator
from networkx import MultiDiGraph, write_gpickle

from activities.config import timezone
from activities.utils import decode_json
from activities.nlp.parsers import PriceParser
from activities.database.redis import db, Event


headers = {
    "Host": "opendata.paris.fr",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}
price_parser = PriceParser()


def get_event_from_row(row: dict) -> Optional[Event]:

    identifier = row.get('id', None)
    if not identifier:
        return

    title = row.get('title', None)
    if not title:
        return

    raw_tags = row.get('tags', None)
    if not raw_tags:
        return
    tags = ';'.join([
        tag.lower().replace('-', '_').replace(' ', '_')
        for tag in raw_tags.split(';')
    ])

    # Process reservation info
    reservation_required_val = row.get('access_type', None)
    if not reservation_required_val:
        return
    reservation_map = {
        'non': 0,
        'conseillée': 1,
        'obligatoire': 1,
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
    occurrences_start_end = []
    for occ in occurrences:
        occ_parts = occ.split('_')
        if len(occ_parts) == 1:
            occurrences_start_end.append((occ, occ))
        elif len(occ_parts) == 2:
            start, end = occ_parts
            occurrences_start_end.append((start, end))
        else:
            print(f'Too much dates: {occ}')
            continue
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
        return
    if price_type == 'payant':
        price_found = price_parser(price_detail)
        if price_found is None:
            # We did not find any price
            # TODO: Edge cases:
            #  - "Sur réservation"
            return
        else:
            price_start, price_end = price_found  # Unpack
    else:
        price_start, price_end = 0, 0

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
    zipcode = zipcode[:5]
    department = int(zipcode[:2])
    district = zipcode[-2:] if zipcode.startswith('75') else 0

    lat, lon = row.get('lat_lon', (None, None))
    if not lat or not lon:
        return

    values = dict(
        pk=identifier,

        title=title,
        url=row.get('url', ''),
        tags=tags,

        reservation_required=reservation_required,
        reservation_url=reservation_url,
        reservation_url_description=reservation_url_description,

        date_start=date_start.timestamp(),
        date_end=date_end.timestamp(),

        price_type=price_type,
        price_detail=price_detail,
        price_start=price_start,
        price_end=price_end,

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
        longitude=lon,

        blind=row.get('blind', 0),
        deaf=row.get('deaf', 0),
        pmr=row.get('pmr', 0),
    )
    try:
        event = Event(**values)
    except ValidationError as e:
        print(f'Invalid event: {e}')
        return
    else:
        return event


def get_clean_events(records: list) -> Generator[Event, None, None]:
    for record in records:
        index: int

        event = get_event_from_row(record['fields'])
        if event is not None:
            yield event


def que_faire_a_paris(force: bool = True) -> bool:
    """
    Gets the "Que Faire à Paris ?" dataset and add it to the database.
    This data source is updated every day, around 6-7 AM.
    If the database has already been downloaded today, it is read from disk.
    Source: https://opendata.paris.fr/explore/dataset/que-faire-a-paris-/
    """

    # Get all the event ids we got in the database
    db_record_ids = set()
    for key in db.scan_iter('*'):
        _, prefix, key, *suffix = key.split(':')
        db_record_ids.update({key})
    print(f'{len(db_record_ids)} events currently in the database.')

    # If the database is empty, force pull
    if len(db_record_ids) == 0:
        force = True

    if not force:
        last_save = db.lastsave()
        now = datetime.now(timezone)
        last_update = datetime(year=now.year, month=now.month, day=now.day, hour=7)
        if last_save > last_update:
            print(f'Data was already modified earlier this day ({last_save}), skipping pull')
            return False

    endpoint = "https://opendata.paris.fr/api/records/1.0/search/"
    # Searches for the 10k first events, with the timezone set on Paris.
    params = {
        'dataset': 'que-faire-a-paris-',
        'q': '',
        'rows': 10_000,
        'timezone': 'Europe/Paris'
    }

    with requests.get(endpoint, params=params, headers=headers) as r:
        data = decode_json(r.text)

    inserted = 0
    for record in data['records']:
        if record['fields']['id'] in db_record_ids:
            continue
        event = get_event_from_row(record['fields'])
        if event is not None:
            event.save()
            inserted += 1

    db.save()
    print(f'{inserted} events inserted in the database')
    return True


def download_conceptnet():
    """
    Downloads a subset of ConceptNet (https://conceptnet.io/)
    and construct a usable graph, which is then stored on disk.
    """

    def _get_tag(tag: str):
        """
        Downloads the information linked to the tag, and returns a format which
        can be easily added to the existing graph.
        """
        params = {
            'start': f'/c/fr/{tag}',
            'other': '/c/fr',  # Only keep results in French
            'limit': 5000
        }
        with requests.get('https://api.conceptnet.io/query', params=params) as r:
            info = decode_json(r.text)

            nodes = set()
            edges = []
            for edge in info['edges']:
                node_start = edge['start']['label']
                node_end = edge['end']['label']
                nodes.update({node_start, node_end})
                edges.append((
                    node_start, node_end, edge['rel']['label'], edge['weight'],
                ))
        return nodes, edges

    # Get all the tags from the database
    tags = set()
    for pk in Event.all_pks():
        event = Event.get(pk)
        tags.update(event.tags.split(';'))
    print(f'Found {len(tags)} tags: {tags}')

    # Create the graph
    graph = MultiDiGraph()
    # and populate it
    for tag in tags:
        nodes, edges = _get_tag(tag)
        graph.add_nodes_from(nodes)
        for edge in edges:
            u, v, key, weight = edge
            graph.add_edge(u, v, key=key, weight=weight)
    print(f'Got {len(graph.nodes)} nodes and {len(graph.edges)} edges')

    write_gpickle(graph, 'conceptnet.gpickle')
    print('Wrote graph on disk')


if __name__ == "__main__":
    was_updated = que_faire_a_paris()
    Migrator().run()
    if was_updated:
        download_conceptnet()
