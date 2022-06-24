"""
Implements a Redis database to interact with a server.

Redis resources:
- https://realpython.com/python-redis/
- https://redis.io/commands/
"""

import json

from typing import List
from pydantic import HttpUrl
from datetime import datetime
from redis_om import JsonModel, Field, Migrator, get_redis_connection

from ..utils import get_redis_password
from ..config import (redis_server_address, redis_server_port,
                      redis_server_config, timezone)


db = get_redis_connection(
    host=redis_server_address,
    port=redis_server_port,
    password=get_redis_password(),
    db=0,
    **redis_server_config,
)
db.ping()


Migrator().run()


class Event(JsonModel):
    """
    Represents an event, which is a line in the `que-faire-a-paris-` dataset.
    Each field must have the same name as in the table.
    """

    # TODO: uncomment attributes and add them in `pull_data.py`.

    title: str
    #description: str
    #lead_text: str
    url: HttpUrl
    tags: List[str] = Field(index=True)

    reservation_required: int  # 1 = yes ; 0 = no. See below for why no bool
    reservation_url: str
    reservation_url_description: str

    # TODO: Convert to datetime objects when supported
    date_start: int = Field(index=True)
    date_end: int = Field(index=True)
    #occurrences: str
    #date_description: str

    price_type: str
    price_detail: str
    price_start: float = Field(index=True)
    price_end: float = Field(index=True)

    # FIXME: Set right types when
    # https://github.com/redis/redis-om-python/issues/254 is fixed
    contact_url: str
    contact_mail: str
    contact_phone: str
    contact_facebook: str
    contact_twitter: str

    place: str
    street: str
    city: str
    zipcode: str
    department: int
    district: int = Field(index=True)

    latitude: float = Field(index=True)
    longitude: float = Field(index=True)

    # Following fields should be booleans, but it is not yet supported.
    # See https://github.com/redis/redis-om-python/issues/193
    blind: int
    deaf: int
    pmr: int  # Personne à Mobilité Réduite

    class Meta:
        database = db

    def to_json(self) -> dict:
        info = json.loads(self.json())
        # Convert timestamps to datetime objects
        info['date_start'] = datetime.fromtimestamp(info['date_start'], tz=timezone)
        info['date_end'] = datetime.fromtimestamp(info['date_end'], tz=timezone)
        return info
