from __future__ import annotations

import spacy

from collections import Counter


from .request import Request
from .utils import decode_json


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
        # Load the French accurate pipeline
        self._nlp = spacy.load('fr_dep_news_trf')
        self.request = Request()

    def interpret_user_input(self, user_input: str) -> bool:
        """
        Takes a string - the sentence input by the user - interprets it,
        and returns True if it has been interpreted successfully,
        False otherwise.
        """
        # Process the user input with the NLP pipeline
        document = self._nlp(user_input)

        labels = Counter([doc.label_ for doc in document.ents])
        labels = sorted(labels, reverse=True)
        # In `labels` the first is the most common, the last the least.

        return False

    @classmethod
    def from_json(cls, cookie: str) -> Model:
        """
        Takes information about a model, as a JSON-encoded string,
        and construct a model from this data.
        The string can be empty, in which case a new model is created.
        """
        model = cls()
        for key, value in decode_json(cookie):
            model.__setattr__(key, value)
        return model

    def to_json(self) -> str:
        """
        Returns this model as a JSON-encoded string, which can then be stored
        in a user cookie.
        """
        return vars(self)
