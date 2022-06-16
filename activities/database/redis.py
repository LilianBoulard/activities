"""
Implements a Redis database to interact with a server.

Redis resources:
- https://realpython.com/python-redis/
- https://redis.io/commands/
"""

import datetime

from typing import Optional
from pydantic import EmailStr, HttpUrl
from redis_om import HashModel, Field, Migrator, get_redis_connection

from ..config import redis_server_address, redis_server_port, redis_server_config


db = get_redis_connection(
    host=redis_server_address,
    port=redis_server_port,
    db=0,
    **redis_server_config,
)
db.ping()


Migrator().run()


class Event(HashModel):
    """
    Represents an event, which is a line in the `que-faire-a-paris-` dataset.
    Each field must have the same name as in the table.
    """

    # TODO: uncomment attributes and add them in `pull_data.py`.

    title: str
    #description: str
    #lead_text: str
    url: HttpUrl
    tags: str = Field(index=True)

    reservation_required: int  # 1 = yes ; 0 = no. See below for why no bool
    reservation_url: str
    reservation_url_description: str

    date_start: datetime.datetime = Field(sortable=True)
    date_end: datetime.datetime = Field(sortable=True)
    #occurrences: str
    #date_description: str

    price_type: str
    price_detail: str
    price_start: float = Field(sortable=True)
    price_end: float = Field(sortable=True)

    contact_url: Optional[HttpUrl]
    contact_mail: Optional[EmailStr]
    contact_phone: Optional[str]
    contact_facebook: Optional[HttpUrl]
    contact_twitter: Optional[HttpUrl]

    place: str
    street: str
    city: str
    zipcode: str
    department: int
    district: int = Field(index=True)

    latitude: float
    longitude: float

    # Following fields should be booleans, but it is not yet supported.
    # See https://github.com/redis/redis-om-python/issues/193
    blind: int
    deaf: int
    pmr: int  # Personne à Mobilité Réduite

    class Meta:
        database = db

    def to_json(self) -> dict:
        return self.dict()
