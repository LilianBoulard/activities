"""
Implements a request capable of querying the database, given some criterion.
"""

from functools import reduce
from datetime import date as Date
from typing import List, Optional

from .utils import encode_json, decode_json
from .database.sql import Event
from sqlalchemy import and_, or_


class Request:

    """
    Represents a request to the database.
    To use it, instantiate it, and update its attributes
    (which are empty by default).
    At any point during this process, you can use the `query` method to return
    the objects corresponding to the set criterion.

    Currently, it can query given the following criterion:
        - Date range
        - Tag(s)
        - Price range
        - Geographical location
            - Longitude / latitude
            - City district
    """

    # Price criterion
    price_lower_bound: Optional[float] = None
    price_upper_bound: Optional[float] = None

    # Date criterion
    date_lower_bound: Optional[Date] = None
    date_upper_bound: Optional[Date] = None

    # Theme / tag / type criterion
    tags: Optional[List[str]] = None

    # Location criterion
    district: Optional[int] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None

    def __init__(self):
        pass

    def query(self) -> List[Event]:
        """
        Queries the database, returning the list of events matching the
        criterion set in this instance.
        """
        # List containing the parameters for the final query.
        criterion = []

        # Price criteria
        if self.price_lower_bound is not None and self.price_upper_bound is not None:
            criterion.append(or_(
                and_(self.price_lower_bound <= Event.price_start, Event.price_start <= self.price_upper_bound),
                and_(self.price_lower_bound <= Event.price_end, Event.price_end <= self.price_upper_bound),
            ))

        # Date criteria
        if self.date_lower_bound is not None and self.date_upper_bound is not None:
            criterion.append(or_(
                and_(self.date_lower_bound <= Event.date_start, Event.date_start <= self.date_upper_bound),
                and_(self.date_lower_bound <= Event.date_end, Event.date_end <= self.date_upper_bound),
            ))

        # Tags criteria
        if self.tags is not None:
            # For each tag, create a criteria and "and" all of them together.
            # For example, if we got two tags, "concert" and "jazz",
            # the final criteria (`tags_criteria`) is equivalent to doing
            # `"concert" in Event.tags and "jazz" in Event.tags`
            tags_criterion = []
            for tag in self.tags:
                tags_criterion.append(tag in Event.tags)
            criterion.append(and_(tags_criterion))

        # Location criteria
        if self.district is not None:
            criterion.append(Event.district == self.district)

        events = Event.query(*criterion)
        return events

    @classmethod
    def from_json(cls, info: str):
        req = cls()
        # Set all values in info programmatically
        for key, value in decode_json(info):
            req.__setattr__(key, value)
        return req

    def to_json(self):
        return encode_json(vars(self))
