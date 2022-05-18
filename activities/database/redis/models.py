import datetime

from typing import Tuple

from redis_om import HashModel
from pydantic import EmailStr, HttpUrl


class Event(HashModel):
    """
    Represents an event, which is a line in the `que-faire-a-paris-` dataset.
    Each field must have the same name as in the table.
    """

    title_event: str
    description: str
    lead_text: str
    url: HttpUrl
    tags: str

    access_type: str  # Is reservation necessary
    access_link: str  # Reservation URL
    access_link_text: str  # Reservation URL description

    date_start: datetime.date
    occurrences: str
    date_description: str

    price_type: str
    price_detail: str

    contact_url: HttpUrl
    contact_mail: EmailStr
    contact_phone: str
    contact_facebook: HttpUrl
    contact_twitter: HttpUrl

    address_name: str
    address_street: str
    address_city: str
    address_zipcode: str

    lat_lon: Tuple[float, float]

    blind: bool
    deaf: bool
    pmr: bool  # Personne à Mobilité Réduite
