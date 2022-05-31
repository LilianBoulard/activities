"""
Gets data from opendata.paris.fr and stores them in the Redis database.
"""

import requests
import pandas as pd
import re

from typing import Dict, List, Any, Optional
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


def get_event_from_row(row: pd.Series) -> Optional[Event]:

    if row['Date de début'] is None:
        return

    if row['Date de fin'] is None:
        return

    if row['Coordonnées géographiques'] is None:
        return

    if row['Mots clés'] is None:
        return

    url_dataparis = row["URL"]
    url_event = row["Url de contact"]
    title = row["Title"]
    date_start = row["Date de début"]
    date_end = row["Date de fin"]
    occurence = row["Occurrences"]
    tags = row["Mots clés"]
    lieu = row["Nom du lieu"]
    cp = row["Code postal"]
    ville = row["Ville"]
    long_lat = row["Coordonnées géographiques"]
    h_pmr = row["Accès PMR"]
    h_m_voyant =  row["Accès mal voyant"]
    h_m_entendant = row["Accès mal entendant"]
    transport = row["Transport"]
    tel = row["Téléphone de contact"]
    mail = row["Email de contact"]
    type_prix = row["Type de prix"]
    resa = row["Type d'accès"]
    url_resa = row["URL de réservation"]

    code_postal = row["Code postal"]
    if code_postal.startswith('75'):
        arrondissement = code_postal[-2:]
    else:
        arrondissement = 0

    departement = row["Code postal"][:2]
    
    #  prix_range = JE SAIS PAS QUOI METTTRE
    # Regex pour récupérer que les prix : ([0-9]+(\.|,)[0-9]+|[0-9]+)( ?)(a|à|-)( ?)([0-9]+(\.|,)[0-9]+|[0-9]+)( ?)(€|eur|EUR|euos)|([0-9]+(\.|,)[0-9]+)( ?)(€|eur|EUR|euos)|([0-9]+)( ?)(€|eur|EUR|euos)|(€|eur|EUR|euos)( ?)[0-9]+
    # Regex pour ne garder que les chiffres : [0-9]+(\.|,)[0-9]+|[0-9]+
    # L'idée est de caler dans une colonne le chiffre min matché par la regex précédente
    # De la même manière une colonne max avec cette même regex
    if type_prix == 'payant':
        all = re.match('([0-9]+(\.|,)[0-9]+|[0-9]+)( ?)(a|à|-)( ?)([0-9]+(\.|,)[0-9]+|[0-9]+)( ?)(€|eur|EUR|euos)|([0-9]+(\.|,)[0-9]+)( ?)(€|eur|EUR|euos)|([0-9]+)( ?)(€|eur|EUR|euos)|(€|eur|EUR|euos)( ?)[0-9]+)',row['Détail du prix'])
        all_prix = []
        
        for i in all:
            temp = list(set(i))
            temp.remove('')
            price = re.search(r'[0-9]+(\.|,)[0-9]+|[0-9]+',''.join(temp))
            all_prix.append(int(price.group()))
                

    return Event(
        url_dataparis = url_dataparis,
        url_event = url_event,
        title = title,
        date_start = date_start,
        date_end = date_end,
        occurence = occurence,
        tags = tags,
        lieu = lieu,
        cp = cp,
        departement = departement,
        arrondissement = arrondissement,
        ville = ville,
        long_lat = long_lat,
        h_pmr = h_pmr,
        h_m_voyant = h_m_voyant,
        h_m_entendant = h_m_entendant,
        transport = transport,
        tel = tel,
        mail = mail,
        type_prix = type_prix,
        prix_min = min(all_prix),
        prix_max = max(all_prix),
        prix_range = prix_range,
        resa = resa,
        url_resa = url_resa
    )



def get_clean_events(df: pd.Dataframe) -> List[Event]:
    clean_events: List[Event] = []

    for index, row in df.iterrows():
        index: int
        row: pd.Series

        event = get_event_from_row(row)
        if event is not None:
            clean_events.append(event)

    return clean_events


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
