from random import choice
from functools import wraps
from typing import Callable, Set, Tuple

from .nlp.parsers import DateParser


class Template:

    """
    Constructs answers for the bot.
    FIXME: this is disgusting, find another way of doing that.
    """

    prefixes = [
        'Cool ! ',
        'Reçu 5/5, ',
        'Donc ',
    ]
    _type_default = 'un évènement '
    _date_parts = [
        'entre le {date_min} et le {date_max}',
        'autour du {date_min} au {date_max}',
    ]
    _price_parts = [
        'entre {price_min} et {price_max} €',
        'autour de {price_min}-{price_max} €',
    ]
    suffixes = [
        ', ça roule !',
        ", c'est noté !",
        ', je note 🧐',
    ]
    default_format = '{prefix} {type} {date} {price}{suffix}'

    sorry_prefix = [
        'Désolé, ',
        'Navré, ',
        'Sorry 😅, ',
    ]
    sorry = [
        "je n'ai pas compris ce que tu voulais dire, peux-tu s'il te plait reformuler ?",
        "je ne suis pas en mesure de t'aider pour ça !",
    ]
    error_format = "{prefix}{sorry}"

    def __init__(self):
        pass

    def get_sorry(self) -> str:
        prefix = choice(self.sorry_prefix)
        sorry = choice(self.sorry)
        return self.error_format.format(prefix=prefix, sorry=sorry)

    def __call__(self, request: "Request", updated_attributes: Set[str]) -> Tuple[bool, str]:
        if len(updated_attributes) == 0:
            return False, self.get_sorry()

        prefix = choice(self.prefixes)
        suffix = choice(self.suffixes)

        if not request.tags:
            event = self._type_default
        else:
            event = ' ou '.join(request.tags)

        if (request.date_lower_bound is None) or (request.date_upper_bound is None):
            date = ''
        else:
            dp = DateParser()
            date = choice(self._date_parts).format(
                date_min=dp.as_readable_date(request.date_lower_bound),
                date_max=dp.as_readable_date(request.date_upper_bound),
            )

        if (request.price_lower_bound is None) or (request.price_upper_bound is None):
            price = ''
        else:
            price = choice(self._price_parts).format(
                price_min=request.price_lower_bound,
                price_max=request.price_upper_bound,
            )

        return True, self.default_format.format(
            prefix=prefix, type=event, date=date, price=price, suffix=suffix,
        )


class Answer:
    """
    Stateless class used to get a natural language answer from a query.
    It is meant to be used as the decorator of the method
    `Model.interpret_user_input` and will not work in other settings.
    Returns (1) a boolean indicating whether something could be interpreted
    from the user input, and (2) a corresponding answer.
    """

    templater = Template()

    def __call__(self, func: Callable[["Model", str], Set[str]]) -> Callable[["Model", str], Tuple[bool, str]]:
        @wraps(func)
        def wrapper(instance: "Model", user_input: str):
            updated_attributes = func(instance, user_input)
            return self.templater(instance.request, updated_attributes)
        return wrapper
