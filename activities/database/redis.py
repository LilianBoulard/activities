"""
Implements a Redis database to interact with a server.

Redis resources:
- https://realpython.com/python-redis/
- https://redis.io/commands/
"""

import datetime

from pydantic import EmailStr, HttpUrl
from redis_om import HashModel, Field, Migrator, get_redis_connection

from ..config import redis_server_address, redis_server_port, redis_server_config


db = get_redis_connection(
    host=redis_server_address,
    port=redis_server_port,
    **redis_server_config,
)


Migrator().run()


class Event(HashModel):
    """
    Represents an event, which is a line in the `que-faire-a-paris-` dataset.
    Each field must have the same name as in the table.
    """

    # TODO: uncomment attributes and add them in `pull_data.py`.

    identifier: int = Field(index=True, primary_key=True)

    title: str
    #description: str
    #lead_text: str
    url: HttpUrl
    tags: str

    reservation_required: bool
    reservation_url: str
    reservation_url_description: str

    date_start: datetime.datetime
    date_end: datetime.datetime
    #occurrences: str
    #date_description: str

    price_type: str
    price_detail: str
    price_start = float
    price_end = float

    contact_url: HttpUrl
    contact_mail: EmailStr
    contact_phone: str
    contact_facebook: HttpUrl
    contact_twitter: HttpUrl

    place: str
    street: str
    city: str
    zipcode: str
    department: int
    district: int

    latitude: float
    longitude: float

    blind: bool
    deaf: bool
    pmr: bool  # Personne à Mobilité Réduite

    class Meta:
        database = db
