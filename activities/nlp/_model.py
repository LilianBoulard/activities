"""
Implements the Natural Language Processing functionalities.

Resources:
- Named Entity Recognition
    - https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
- Dependency parsing
    - https://universaldependencies.org/u/dep/
    - https://machinelearningknowledge.ai/learn-dependency-parser-and-dependency-tree-visualizer-in-spacy/
"""

from __future__ import annotations

from ._nlp import NLP
from ..request import Request
from .parsers.date import DateParser
from .parsers.type import TypeParser
from ..utils import encode_json, decode_json


class Model:

    """
    This class is instantiated every time a user reloads the page.
    It will be kept along the conversation.

    Each time the user sends a message, it is passed to the method
    `interpret_user_input`, which interprets its content.
    If some useful information could be extracted, the inner request is updated.
    This request, which is used to create the query to the database, can be
    acquired with the attribute `request`.

    """

    def __init__(self):
        # Load tokenizer, tagger, parser and NER
        self._nlp = NLP()
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

        for entity in document:

            # Process the date
            if entity['entity_group'] == 'DATE':
                date_parser = DateParser()
                date_range = date_parser(entity['word'])
                if date_range is not None:
                    date_start, date_end = date_range  # Unpack
                    self.request.date_lower_bound = date_start
                    self.request.date_upper_bound = date_end
                    understood_something = True
                    #print(date_start, date_end, understood_something)
                continue

            # Process the type
            if entity['entity_group'] == 'DATE':
                #type_parser = TypeParser()
                #extracted_type = type_parser(entity['word'])
                continue

            # Process the price
            if entity['entity_group'] == 'MONEY':
                # TODO
                continue

        return understood_something

    @classmethod
    def from_json(cls, info: str) -> Model:
        """
        Takes information about a model, as a JSON-encoded string,
        and construct a model from this data.
        The string can be empty, in which case a new model is created.
        """
        info_dec = decode_json(info)
        # Instantiate with language
        model = cls()
        # Set the request
        model.request = Request.from_json(info_dec.pop('request'))
        return model

    def to_json(self) -> str:
        """
        Returns this model as a JSON-encoded string, which can then be stored
        in a user cookie.
        """
        return encode_json({
            'request': self.request.to_json(),
        })
