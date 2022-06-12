import datetime

from redis_om import HashModel
from pydantic import EmailStr, HttpUrl


class Event(HashModel):
    """
    Represents an event, which is a line in the `que-faire-a-paris-` dataset.
    Each field must have the same name as in the table.
    """

    # TODO: uncomment attributes and add import them in `pull_data.py`.

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
