import pandas as pd

from typing import Optional, Tuple, Dict, Callable
from Levenshtein import distance
from datetime import datetime


def minmax(func):
    """
    Function used to decorate methods returning the two `datetime`s.
    It sets the hour of the start date to midnight, and the time of the
    end date at 11:59PM (min start, max end).
    """
    def wrapper(*args, **kwargs):
        date_start, date_end = func(*args, **kwargs)
        # TODO
        return date_start, date_end
    return wrapper


class BaseDateRangeParser:

    """
    Base date range parser.

    Parameters
    ----------

    parent_parser: DateParser
        DateParser instantiating this class.

    Attributes
    ----------

    parent_parser: DateParser
        Reference to the parser that instantiated this class.

    ranges: Dict[str, Callable]
        Maps recognized ranges to a callable that returns a tuple of two dates
        (start and end dates).

    valid_threshold: int
         If the distance is strictly superior to this threshold,
         then it's a miss. If it's inferior or equal, it's a match.

    """

    # Technical note: `ranges` must be at the end of the class,
    # otherwise it's not possible to reference the methods in the dictionary.
    ranges: Dict[str, Callable]
    valid_threshold: int = 3

    def __init__(self, parent_parser: "DateParser"):
        self._parent: "DateParser" = parent_parser

    def __call__(self, date_range: str) -> Optional[Tuple[datetime, datetime]]:
        """
        Takes a date range as a string, and returns a tuple of two `datetime`
        if it could be parsed. Otherwise, it returns None.
        """
        # Compute the distance between the input string and the
        # supported ranges
        distances = pd.DataFrame([
            (expression, distance(date_range, expression))
            for expression in self.ranges.keys()
        ], columns=['range', 'distance'])

        if (distances['distance'] > self.valid_threshold).all():
            # The input string doesn't match any range.
            return

        # Return the range name with the lowest distance from the input string
        return distances[distances['distance'].idxmin()]['range']

    def _try_get_exact(self, date_string: str) -> Optional[datetime]:
        """Helper method"""
        return self._parent._try_get_exact(date_string)
