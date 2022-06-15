import pandas as pd
import parsedatetime as pdt

from datetime import datetime, timedelta
from Levenshtein import distance
from typing import Tuple, Optional, Dict, Callable

from ...config import timezone


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


class DateRangeParser:

    """
    French date range parser.

    Parameters
    ----------

        parent_parser: DateParser
            Reference to the parser that instantiated this class.

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
    valid_threshold: int = 3

    def __init__(self, parent_parser):
        self._parent: DateParser = parent_parser

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
        ], columns=['range', 'distance']).set_index('range')

        if (distances['distance'] > self.valid_threshold).all():
            # The input string doesn't match any range.
            return

        # Return the range name with the lowest distance from the input string
        return self.ranges[distances['distance'].idxmin()](self)

    def _try_get_exact(self, date_string: str) -> Optional[datetime]:
        """Helper method"""
        return self._parent._try_get_exact(date_string)

    @minmax
    def _cette_semaine(self) -> Tuple[datetime, datetime]:
        weekday = datetime.now().weekday()
        if 0 <= weekday <= 4:
            # We're between monday and friday
            date_start = self._try_get_exact('samedi')
            date_end = self._try_get_exact('dimanche')
        else:
            # It's the weekend
            date_start = self._try_get_exact('lundi')
            date_end = self._try_get_exact("dimanche prochain")
        if date_end < date_start:
            print(f'Got incoherent dates: start={date_start}, end={date_end}')
        return date_start, date_end

    @minmax
    def _semaine_prochaine(self) -> Tuple[datetime, datetime]:
        date_start = self._try_get_exact('lundi prochain')
        date_end = self._try_get_exact('dimanche prochain') + timedelta(days=7)
        if date_end < date_start:
            print(f'Got incoherent dates: start={date_start}, end={date_end}')
        return date_start, date_end

    @minmax
    def _ce_week_end(self) -> Tuple[datetime, datetime]:
        weekday = datetime.now().weekday()
        if 0 <= weekday <= 4:
            # We're between monday and friday
            date_start = self._try_get_exact('samedi')
            date_end = self._try_get_exact('dimanche')
        elif weekday == 5:
            # It's saturday
            date_start = self._try_get_exact("aujourd'hui")
            date_end = self._try_get_exact('demain')
        else:
            # It's sunday
            date_start = self._try_get_exact('hier')
            date_end = self._try_get_exact("aujourd'hui")
        if date_end < date_start:
            print(f'Got incoherent dates: start={date_start}, end={date_end}')
        return date_start, date_end

    @minmax
    def _week_end_prochain(self) -> Tuple[datetime, datetime]:
        date_start = self._try_get_exact('samedi prochain')
        date_end = self._try_get_exact('dimanche prochain')
        if date_end < date_start:
            print(f'Got incoherent dates: start={date_start}, end={date_end}')
        return date_start, date_end

    ranges: Dict[str, Callable] = {
        'cette semaine': _cette_semaine,
        'semaine prochaine': _semaine_prochaine,
        'ce week-end': _ce_week_end,
        'week-end prochain': _week_end_prochain,
    }


class DateParser:
    """
    Used to parse a natural language date.

    Supports both exact dates (down to the hour),
    and date ranges (down to the hour as well).

    Usage
    -----
    >>> date_parser = DateParser()
    >>> dates = date_parser('next week')
    >>> if dates is None: RuntimeError('Could not parse input')
    >>> date_start, date_end = dates
    """

    def __init__(self):
        self.range_parser = DateRangeParser(parent_parser=self)
        self.cal = pdt.Calendar(pdt.Constants(localeID="fr_FR"))

    def _try_get_exact(self, date_input: str) -> Optional[datetime]:
        """
        Takes a date input, and returns a list of `datetime` if it could be
        parsed. Otherwise, returns None.
        The `datetime` objects represent exact times, and not ranges.
        This means that
        """
        date_parts = self.cal.parseDT(date_input, tzinfo=timezone)

        *dates, parsed_type = date_parts
        if parsed_type == 0:
            # Could not parse, invalid input
            return

        if len(dates) > 1:
            print(f'Parsed multiple datetime objects from {date_input}')

        parsed_date = dates[0]

        # Convert the parsed dates to datetime type.
        to_datetime_funcs = {
            1: lambda _date: datetime.fromisoformat(_date.isoformat()),
            2: lambda _time: datetime.fromisoformat(_time.isoformat()),
            3: lambda _datetime: _datetime,
        }
        parsed_date = to_datetime_funcs[parsed_type](parsed_date)

        return parsed_date

    def _try_get_range(self, date_input: str) -> Optional[Tuple[datetime, datetime]]:
        """
        Tries to parse the passed string to find a date range.
        """
        return self.range_parser(date_input)

    def __call__(self, date_string: str) -> Optional[Tuple[datetime, datetime]]:
        """
        Takes a date as a string, and returns the date start and the date end.
        The parsing tries to be clever about dates and their usage in the
        context of the project.
        """
        date_start, date_end = None, None

        # First, tries to get specific dates from the input
        exact_date = self._try_get_exact(date_string)
        if exact_date is not None:
            pass
        else:
            # Exact parsing didn't result in anything usable
            pass

        # Secondly, tries to get a range from the input
        date_range = self._try_get_range(date_string)
        if date_range is not None:
            date_start, date_end = date_range
        else:
            # Range parsing didn't result in anything usable
            pass

        if not date_start or not date_end:
            return

        return date_start, date_end
