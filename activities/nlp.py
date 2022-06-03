"""
Implements the Natural Language Processing functionalities.

Resources:
- Named Entity Recognition
    - https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
- Dependency parsing
    - https://universaldependencies.org/u/dep/
"""

from __future__ import annotations

import spacy

from .request import Request
from .utils import encode_json, decode_json, zip_to_dict
from .design import Singleton, apply_init_callback_to_singleton


def load_nlp(instance):
    instance.nlp = spacy.load('fr_dep_news_trf')


@apply_init_callback_to_singleton(load_nlp)
class NLP(Singleton):
    """
    Magic singleton class used to hold the spacy NLP pipeline(s)
    in a single location.
    Advantages:
    - Faster model creation, because we don't need to load the NLP each time
    - Better memory efficiency, because we don't have a unique NLP in each session

    Holds the NLP pipelines used to extract information from user input.
    """

    def __call__(self, user_input: str) -> spacy.Language:
        return self.nlp(user_input)


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
        # Load French tokenizer, tagger, parser and NER
        self._nlp = NLP()
        self.request = Request()

    def interpret_user_input(self, user_input: str) -> bool:
        """
        Takes a string - the sentence input by the user - interprets it,
        and returns True if it has been interpreted successfully,
        False otherwise.
        """
        # Process the user input with the NLP pipeline
        document = self._nlp(user_input)

        # Convert the text and labels to a dictionary mapping each label to a
        # list of texts.
        labels = zip_to_dict([(ent.text, ent.label_) for ent in document.ents])

        # Process the date

        # Process the type

        # Process the price

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
            model.request.__setattr__(key, value)
        return model

    def to_json(self) -> str:
        """
        Returns this model as a JSON-encoded string, which can then be stored
        in a user cookie.
        """
        return encode_json(vars(self.request))
