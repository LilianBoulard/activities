"""
Gets data from opendata.paris.fr and stores them in the Redis database.
"""

import requests

from typing import Dict, List, Any
from datetime import datetime

from activities.database.redis import RedisDatabase, Event
from activities.utils import decode_json


headers = {
    "Host": "opendata.paris.fr",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}


def que_faire_a_paris() -> None:
    """
    Gets the "Que Faire à Paris ?" dataset and add it to the database.
    This data source is updated everyday, around 6-7 AM.
    If the database has already been downloaded today, it is read from disk.
    Source: https://opendata.paris.fr/explore/dataset/que-faire-a-paris-/
    """
    if RedisDatabase.dbfilename.exists():
        # If the database file was modified for the last time before the last
        # time the data source was updated (on the website),
        # reset the database and add the new data to it.
        last_mod_time = RedisDatabase.dbfilename.lstat().st_mtime
        last_mod = datetime.fromtimestamp(last_mod_time)
        now = datetime.now()
        last_datasource_update = datetime(now.year, now.month, now.day, hour=7)
        if last_mod > last_datasource_update:
            reset_db = True
        else:
            reset_db = False
    else:
        reset_db = False

    rdb: RedisDatabase = RedisDatabase()
    # If we realize that the db is empty, we'll add the new data regardless.
    if not rdb.is_empty():
        if reset_db:
            rdb.reset()
            RedisDatabase.dbfilename.unlink()
        else:
            return
    # Searches for the 10k first events, with the timezone set on Paris.
    endpoint = ("https://opendata.paris.fr/api/records/1.0/search/"
                "?dataset=que-faire-a-paris-&q="
                "&rows=10000"
                "&timezone=Europe%2FParis")

    with requests.get(endpoint, headers=headers) as r:
        data = decode_json(r.text)

    records: List[Dict[str, Any]] = data['records']
    events: List[Event] = [
        Event(**rec['fields']) for rec in records
    ]
    rdb.bulk_add(events)
    rdb.save()


if __name__ == "__main__":
    que_faire_a_paris()
