import re

from typing import Optional, Tuple


_euro = "€|eur|EUR|euros|euro|Euro|Euros|balles"
price_regex = f'(\\d+(\\.|,)\\d+|\\d+)( ?)(a|à|-)( ?)(\\d+(\\.|,)\\d+|\\d+)( ?)|(\\d+(\\.|,)\\d+)( ?)({_euro})|(\\d+)( ?)({_euro})|({_euro})( ?)(\\d+)'


class PriceParser:

    """
    Takes a sentence and parses it to find prices.
    Currently, uses a regex.
    """

    def _clean_match(self, match: str) -> str:
        return match.replace(',', '.')

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

        return min(all_prices), max(all_prices)
