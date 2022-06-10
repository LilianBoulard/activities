from spacy.tokens import Doc
from spacy import Language, load


def load_nlp(instance, pipeline_name: str):
    """
    Used to set the language of the NLP pipeline.
    `pipeline_name` can be any of the pretrained Spacy pipelines.
    See https://spacy.io/models
    """
    instance.nlp = load(pipeline_name)


class NLP:
    """
    Magic singleton class used to hold the spacy NLP pipeline(s)
    in a single location.
    Advantages:
    - Faster model creation, because we don't need to load the NLP each time
    - Better memory efficiency, because we don't have a unique NLP in each session

    To support a new language, create a subclass of this class, add both this
    class and the Singleton class as parents, and use the init callback
    `load_nlp` with parameter `pipeline_name`.
    See the decorator for more info on the latter, and check out an example
    of the former in `_fr.py`.
    """

    nlp: Language  # Set by `load_nlp`

    def __call__(self, user_input: str) -> Doc:
        return self.nlp(user_input)
