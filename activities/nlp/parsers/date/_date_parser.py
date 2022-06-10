import parsedatetime as pdt

from datetime import datetime
from typing import Tuple, Optional

from .languages import FrenchDateRangeParser


class DateParser:
    """
    Used to parse a natural language date.

    Supports both exact dates (down to the hour),
    and date ranges (down to the hour as well).

    Parameters
    ----------

    language: str
        Any key from "supported_languages".
        Defines in which language the parser will work.
        This should be inherited from the model that instantiates this class.

    Usage
    -----
    >>> date_parser = DateParser()
    >>> dates = date_parser('next week')
    >>> if dates is None: RuntimeError('Could not parse input')
    >>> date_start, date_end = dates
    """

    supported_languages = {
        "fr": FrenchDateRangeParser,
    }
    _lang_to_pdt_constant = {
        "fr": "fr_FR",
    }

    def __init__(self, language):
        range_parser = self.supported_languages.get(language, None)
        if range_parser is None:
            raise ValueError(f'Unsupported language: {language}')

        self.language = language
        self.range_parser = range_parser(parent_parser=self)
        self.cal = pdt.Calendar(
            pdt.Constants(localeID=self._lang_to_pdt_constant[language]),
        )

    def _try_get_exact(self, date_input: str) -> Optional[datetime]:
        """
        Takes a date input, and returns a list of `datetime` if it could be
        parsed. Otherwise, returns None.
        The `datetime` objects represent exact times, and not ranges.
        This means that
        """
        date_parts = self.cal.parseDT(date_input)

        *dates, parsed_type = date_parts
        if parsed_type == 0:
            # Could not parse, invalid input
            return

        # Convert the parsed dates to datetime type.
        to_datetime_funcs = {
            1: lambda _date: datetime.fromisoformat(_date.to_isoformat()),
            2: lambda _time: datetime.fromisoformat(_time.to_isoformat()),
            3: lambda _datetime: _datetime,
        }
        fitting_func = to_datetime_funcs[parsed_type]
        datetimes = [fitting_func(_date) for _date in dates]

        if len(datetimes) > 1:
            print(f'Parsed multiple datetimes from {date_input}')

        return datetimes[0]

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
