"""
Implements the Natural Language Processing functionalities.

Resources:
- Named Entity Recognition
    - https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
- Dependency parsing
    - https://universaldependencies.org/u/dep/
"""

from __future__ import annotations

from typing import List

from .languages import FRNLP
from ..request import Request
from .parsers.date import DateParser
from ..utils import encode_json, decode_json, zip_to_dict


class Model:

    """
    This class is instantiated every time a user reloads the page.
    It will be kept along the conversation.

    Each time the user sends a message, it is passed to the method
    `interpret_user_input`, which interprets its content.
    If some useful information could be extracted, the inner request is updated.
    This request, which is used to create the query to the database, can be
    acquired with the attribute `request`.

    Parameters
    ----------

    language: str ; default "fr"
        Any key from "supported_languages".
        Defines in which language the parser will work.

    """

    supported_languages = {
        "fr": FRNLP,
    }

    def __init__(self, language: str = "fr"):
        # Load tokenizer, tagger, parser and NER
        pipeline = self.supported_languages.get(language, None)
        if pipeline is None:
            raise ValueError(f'Unsupported language: {language}')

        self.language = language
        self._nlp = pipeline()
        # Create a new request
        self.request = Request()

    def interpret_user_input(self, user_input: str) -> bool:
        """
        Takes a string - the sentence input by the user - interprets it,
        and returns True if it has been interpreted successfully,
        False otherwise.
        """
        understood_something = False

        # Process the user input with the NLP pipeline
        document = self._nlp(user_input)

        # Convert the text and labels to a dictionary mapping each label to a
        # list of texts.
        labels = zip_to_dict([(ent.text, ent.label_) for ent in document.ents])

        # Process the date
        if 'DATE' in labels:
            date_parser = DateParser(language=self.language)
            for date_input in labels['DATE']:
                date_range = date_parser(date_input)
                if date_range is not None:
                    date_start, date_end = date_range  # Unpack
                    self.request.date_lower_bound = date_start
                    self.request.date_upper_bound = date_end
                    understood_something = True

        # Process the type
        unique_types: List[str] = []
        # TODO

        # Process the price
        if 'MONEY' in labels:
            for money_input in labels['MONEY']:
                # TODO
                pass

        return understood_something

    @classmethod
    def from_json(cls, info: str) -> Model:
        """
        Takes information about a model, as a JSON-encoded string,
        and construct a model from this data.
        The string can be empty, in which case a new model is created.
        """
        model = cls()  # TODO: set language depending on info
        for key, value in decode_json(info):
            model.request.__setattr__(key, value)
        return model

    def to_json(self) -> str:
        """
        Returns this model as a JSON-encoded string, which can then be stored
        in a user cookie.
        """
        return encode_json(vars(self.request))
