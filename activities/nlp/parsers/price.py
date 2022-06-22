import re

from typing import Optional, Tuple, List


_euro = "€|eur|EUR|euros|euro|Euro|Euros|balles"
price_regex = f'(\\d+(\\.|,)\\d+|\\d+)( ?)(a|à|-)( ?)(\\d+(\\.|,)\\d+|\\d+)( ?)|(\\d+(\\.|,)\\d+)( ?)({_euro})|(\\d+)( ?)({_euro})|({_euro})( ?)(\\d+)'


class PriceParser:

    """
    Takes a sentence and parses it to find prices.
    Currently, uses a regex.
    """

    # This variable is used when the min price is equal to the max price:
    # in this case, if the value is in the range (1), then some respective
    # offsets are applied to the prices.
    # For example, if we got (min_price=4, max_price=4), and if `_tolerances`
    # had an entry (range(1, 10), (1, 1)), then our final values would be
    # (min_price=3, max_price=5).
    # If the price is not in any range then the last one
    # (assumed to be the highest) is used.
    # See the `_get_tolerance` method for more info.
    _tolerances: List[Tuple[range, Tuple[int, int]]] = [
        (range(1, 10), (1, 1)),
        (range(10, 20), (2, 2)),
        (range(30, 50), (5, 5)),
    ]

    def _clean_match(self, match: str) -> str:
        return match.replace(',', '.')

    def _get_tolerance(self, price: int) -> Tuple[int, int]:
        for rng, tolerance in self._tolerances:
            if price in rng:
                return tolerance
        else:
            return self._tolerances[-1][1]

    def __call__(self, sentence: str) -> Optional[Tuple[int, int]]:

        prices_found = re.findall(price_regex, sentence)

        # FIXME: Hackish
        all_prices = []
        for price_matches in prices_found:
            # Remove duplicates
            matches = list(set(price_matches))
            # Remove empty values
            matches.remove('')
            # Keep only the first integer value
            for match in matches:
                price = self._clean_match(match)
                if price.isnumeric():
                    price = int(price)
                    break
            else:
                # If we did not find any integer value,
                # print a warning and skip this price
                print(f'Match did not contain any valid price: {matches}')
                continue
            all_prices.append(price)

        if not all_prices:
            # We did not find any price
            return

        min_price, max_price = min(all_prices), max(all_prices)
        # If the min/max prices are the same, add a tolerance to each
        if min_price == max_price:
            tolerance_left, tolerance_right = self._get_tolerance(min_price)
            min_price -= tolerance_left
            max_price -= tolerance_right

        return min_price, max_price
