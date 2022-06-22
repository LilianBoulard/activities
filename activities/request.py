"""
Implements a request capable of querying the database, given some criterion.
"""

from functools import reduce
from datetime import datetime
from typing import List, Optional

from .database.redis import Event


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
    date_lower_bound: Optional[datetime] = None
    date_upper_bound: Optional[datetime] = None

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
            criterion.append(
                (self.price_lower_bound <= Event.price_start <= self.price_upper_bound)
                |
                (self.price_lower_bound <= Event.price_end <= self.price_upper_bound)
            )

        # Date criteria
        if self.date_lower_bound is not None and self.date_upper_bound is not None:
            criterion.append(
                (self.date_lower_bound.timestamp() <= Event.date_start <= self.date_upper_bound.timestamp())
                |
                (self.date_lower_bound.timestamp() <= Event.date_end <= self.date_upper_bound.timestamp())
            )

        # Tags criteria
        if self.tags is not None:
            # For each tag, create a criteria and "and" all of them together.
            # For example, if we got two tags, "concert" and "jazz",
            # the final criteria (`tags_criteria`) is equivalent to doing
            # `"concert" in Event.tags and "jazz" in Event.tags`
            tags_criterion = []
            for tag in self.tags:
                tags_criterion.append(tag in Event.tags)
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
        to 4 and 6 respectively, it will return "Entre 4 et 6 €".
        """

        def as_readable_date(dt: datetime) -> str:
            weekday_map = (
                'lundi',
                'mardi',
                'mercredi',
                'jeudi',
                'vendredi',
                'samedi',
                'dimanche',
            )
            weekday = weekday_map[dt.weekday()]

            month_map = (
                'janvier',
                'février',
                'mars',
                'avril',
                'mai',
                'juin',
                'juillet',
                'aout',
                'septembre',
                'octobre',
                'novembre',
                'décembre',
            )
            month = month_map[dt.month - 1]

            return f'{weekday} {dt.day} {month}'

        desc = []
        print(self.to_json())

        if self.price_lower_bound is not None and self.price_upper_bound is not None:
            print('IN !!')
            if self.price_lower_bound == self.price_upper_bound:
                desc.append(f'À {self.price_lower_bound} €')
            else:
                desc.append(f'Entre {self.price_upper_bound} et {self.price_upper_bound} €')

        if self.date_lower_bound is not None and self.date_upper_bound is not None:
            if as_readable_date(self.date_lower_bound) == as_readable_date(self.date_upper_bound):
                desc.append(f'Le {as_readable_date(self.date_lower_bound)}')
            else:
                desc.append(f'Entre le {as_readable_date(self.date_lower_bound)} et le {as_readable_date(self.date_upper_bound)}')

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
            price_lower_bound=lambda val: int(val),
            price_upper_bound=lambda val: int(val),

            date_lower_bound=lambda val: datetime.fromisoformat(val),
            date_upper_bound=lambda val: datetime.fromisoformat(val),

            tags=lambda val: val,

            district=lambda val: int(val),
            latitude=lambda val: float(val),
            longitude=lambda val: float(val),
        )

        # Set all values programmatically
        for field, operation in operations.items():
            value = info.get(field, None)
            if value is not None:
                req.__setattr__(field, operation(value))

        return req

    def to_json(self) -> dict:
        # Init with standard values (not converted to the correct type)
        info = dict(
            price_lower_bound=self.price_lower_bound,
            price_upper_bound=self.price_upper_bound,

            date_lower_bound=self.date_lower_bound,
            date_upper_bound=self.date_upper_bound,

            tags=self.tags,

            district=self.district,
            latitude=self.latitude,
            longitude=self.longitude,
        )

        # Maps a key name to an operation to perform to get the right type
        # This operation will not be executed if the value is None
        operations = dict(
            price_lower_bound=lambda val: val,
            price_upper_bound=lambda val: val,

            date_lower_bound=lambda val: val.isoformat(),
            date_upper_bound=lambda val: val.isoformat(),

            tags=lambda val: val,

            district=lambda val: val,
            latitude=lambda val: val,
            longitude=lambda val: val,
        )

        # Filter out nones and convert to right type
        info = {
            key: operations[key](value)
            for key, value in info.items()
            if value is not None
        }
        return info
