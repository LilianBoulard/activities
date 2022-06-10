from typing import Dict, Callable, Tuple
from datetime import datetime

from ._base import BaseDateRangeParser, minmax


class FrenchDateRangeParser(BaseDateRangeParser):

    """
    French date range parser.
    See BaseDateRangeParser for additional information.
    """

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
        date_end = self._try_get_exact('dimanche prochain')
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
