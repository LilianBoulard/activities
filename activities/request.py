"""
Implements a request capable of querying the database, given some criterion.
"""

from varname import nameof
from functools import reduce
from datetime import datetime
from typing import List, Optional, Set

from .database.redis import Event
from .nlp.parsers import DateParser


def _get_end_of_month() -> datetime:
    # Note: doesn't actually return the end of month,
    # but the beginning of the month right after
    today = datetime.today()

    if today.day > 20:
        month = today.month + 2
    else:
        month = today.month + 1

    # If the target month loops back to 1, increment year
    if month < today.month:
        year = today.year + 1
    else:
        year = today.year

    date = datetime(year, month, 1)
    return date


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
    price_lower_bound: Optional[int] = None
    price_upper_bound: Optional[int] = None

    # Date criterion
    date_lower_bound: Optional[datetime] = datetime.today()
    date_upper_bound: Optional[datetime] = _get_end_of_month()

    # Theme / tag / type criterion
    tags: Optional[Set[str]] = None

    # Location criterion
    district: Optional[int] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None

    def __init__(self):
        pass

    def attributes(self) -> List[str]:
        """
        Returns the list of attributes settable in this request.
        """
        return [
            nameof(self.price_lower_bound),
            nameof(self.price_upper_bound),
            nameof(self.date_lower_bound),
            nameof(self.date_upper_bound),
            nameof(self.tags),
            nameof(self.district),
            nameof(self.longitude),
            nameof(self.latitude),
        ]

    def query(self) -> List[Event]:
        """
        Queries the database, returning the list of events matching the
        criterion set in this instance.
        """
        # List containing the parameters for the final query.
        criterion = []

        # Price criteria
        if self.price_lower_bound is not None and self.price_upper_bound is not None:
            criterion.append(
                (self.price_lower_bound <= Event.price_start <= self.price_upper_bound)
                |
                (self.price_lower_bound <= Event.price_end <= self.price_upper_bound)
            )

        # Date criteria
        if self.date_lower_bound is not None and self.date_upper_bound is not None:
            criterion.append(
                (self.date_lower_bound.timestamp() <= Event.date_start) & (Event.date_start <= self.date_upper_bound.timestamp())
                |
                (self.date_lower_bound.timestamp() <= Event.date_end) & (Event.date_end <= self.date_upper_bound.timestamp())
            )

        # Tags criteria
        if self.tags is not None:
            # For each tag, create a criteria and "and" all of them together.
            # For example, if we got two tags, "concert" and "jazz",
            # the final criteria (`tags_criteria`) is equivalent to doing
            # `"concert" in Event.tags and "jazz" in Event.tags`
            tags_criterion = []
            for tag in self.tags:
                tags_criterion.append(Event.tags << tag)
            if len(tags_criterion) > 0:
                tags_criteria = reduce(lambda occ, elem: occ & elem, tags_criterion)
                criterion.append(tags_criteria)

        # Location criteria
        if self.district is not None:
            criterion.append(Event.district == self.district)

        if len(criterion) > 0:
            criterion_and = reduce(lambda acc, elem: acc & elem, criterion)
            events = Event.find(criterion_and)
        else:
            events = [Event.get(pk) for pk in Event.all_pks()]
        return events

    def get_fields_desc(self) -> List[str]:
        """
        Returns a human-readable description of each completed field.
        For example, if `price_lower_bound` and `price_upper_bound` are set
        to 4 and 6 respectively, it will return ["Entre 4 et 6 €"].
        """
        dp = DateParser()

        desc = []

        if self.price_lower_bound is not None and self.price_upper_bound is not None:
            # We assume both cannot be the same as we added a tolerance
            # (see price parser)
            desc.append(f'Entre {self.price_lower_bound} et {self.price_upper_bound} €')

        if self.date_lower_bound is not None and self.date_upper_bound is not None:
            if dp.as_readable_date(self.date_lower_bound) == dp.as_readable_date(self.date_upper_bound):
                desc.append(f'Le {dp.as_readable_date(self.date_lower_bound)}')
            else:
                desc.append(f'Entre le {dp.as_readable_date(self.date_lower_bound)} et le {dp.as_readable_date(self.date_upper_bound)}')

        if self.tags:
            desc.extend(self.tags)

        if self.district is not None:
            desc.append(f'{self.district}e arrondissement')

        return desc

    @classmethod
    def from_json(cls, info: dict):
        req = cls()

        # Maps a key name to an operation to perform to get the right type
        # This operation will not be executed if the value is None
        operations = dict(
            tags=lambda val: set(val),

            price_lower_bound=lambda val: int(val),
            price_upper_bound=lambda val: int(val),

            date_lower_bound=lambda val: datetime.fromisoformat(val),
            date_upper_bound=lambda val: datetime.fromisoformat(val),

            district=lambda val: int(val),
            latitude=lambda val: float(val),
            longitude=lambda val: float(val),
        )

        for attribute in req.attributes():
            value = info.get(attribute, None)
            if value is None:
                continue
            operation = operations.get(attribute, lambda val: val)
            req.__setattr__(attribute, operation(value))

        return req

    def to_json(self) -> dict:
        # Maps a key name to an operation to perform to get the right type
        # This operation will not be executed if the value is None
        # If no operation is necessary, do not specify any
        operations = dict(
            tags=lambda val: list(val),

            date_lower_bound=lambda val: val.isoformat(),
            date_upper_bound=lambda val: val.isoformat(),
        )

        info = {}
        # Filter out nones and convert to right type
        for attribute in self.attributes():
            value = self.__getattribute__(attribute)
            if value is None:
                continue
            operation = operations.get(attribute, lambda val: val)
            info.update({attribute: operation(value)})

        return info
