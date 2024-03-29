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

from typing import Set
from varname import nameof
from spacy.tokens import Doc

from ._nlp import NLP
from ..answer import Answer
from ..request import Request
from ..utils import encode_json
from .parsers import DateParser, TypeParser, PriceParser


class Model:

    """
    This class is instantiated (reset) every time a user reloads the page.
    It will be kept along the conversation.

    Each time the user sends a message, it is passed to the method
    `interpret_user_input`, which interprets its content.
    If some useful information could be extracted, the inner request is updated.
    This request, which is used to create the query to the database, can be
    acquired with the attribute `request`.

    """

    _answerer = Answer()

    # Instantiate stateless parsers
    date_parser = DateParser()
    type_parser = TypeParser()
    price_parser = PriceParser()

    def __init__(self):
        # Load tokenizer, tagger, parser and NER
        self._nlp = NLP()
        # Create a new request
        self.request = Request()

    @_answerer
    def interpret_user_input(self, user_input: str) -> Set[str]:
        """
        Takes a string - the sentence input by the user - interprets it,
        and returns a list of updated fields in the request.
        When decorated with an answerer, returns a natural language string
        meant to be passed to the user.
        """
        updated_fields = set()

        # Process the user input with the NLP pipeline
        document: Doc = self._nlp(user_input)

        # Try extracting dates from chunks
        for chunk in document.noun_chunks:
            date_range = self.date_parser(chunk.text)
            if date_range is not None:
                # If a date could be extracted, process it
                date_start, date_end = date_range  # Unpack
                self.request.date_lower_bound = date_start
                self.request.date_upper_bound = date_end
                updated_fields.update({
                    nameof(self.request.date_lower_bound),
                    nameof(self.request.date_upper_bound),
                })

        # To process the type, extracts the nouns and lemmatizes them
        lemma_nouns = [word.lemma_ for word in document if word.pos_ == 'NOUN']
        # Remove duplicates
        lemma_nouns = set(lemma_nouns)
        event_types = self.type_parser(lemma_nouns)
        if event_types is not None:
            if self.request.tags is None:
                self.request.tags = event_types
            else:
                self.request.tags.update(event_types)

        # Process the price
        price_found = self.price_parser(user_input)
        if price_found is not None:
            price_start, price_end = price_found  # Unpack
            self.request.price_lower_bound = price_start
            self.request.price_upper_bound = price_end
            updated_fields.update({
                nameof(self.request.price_upper_bound),
                nameof(self.request.price_lower_bound),
            })

        return updated_fields

    @classmethod
    def from_json(cls, info: dict) -> Model:
        """
        Takes information about a model, as a JSON-encoded string,
        and construct a model from this data.
        The string can be empty, in which case a new model is created.
        """
        # Instantiate with language
        model = cls()
        # Set the request
        model.request = Request.from_json(info.pop('request'))
        return model

    def to_json(self) -> str:
        """
        Returns this model as a JSON-encoded string, which can then be stored
        in a user cookie.
        """
        return encode_json({
            'request': self.request.to_json(),
        })
