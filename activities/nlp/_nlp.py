from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

from ..design import Singleton, apply_init_callback_to_singleton


def load_nlp(instance):
    # Load https://huggingface.co/Jean-Baptiste/camembert-ner-with-dates
    tokenizer = AutoTokenizer.from_pretrained(
        "Jean-Baptiste/camembert-ner-with-dates")
    model = AutoModelForTokenClassification.from_pretrained(
        "Jean-Baptiste/camembert-ner-with-dates")
    instance._nlp = pipeline('ner', model=model, tokenizer=tokenizer,
                             aggregation_strategy="simple")


@apply_init_callback_to_singleton(load_nlp)
class NLP(Singleton):
    """
    Magic singleton class used to hold the spacy NLP pipeline(s)
    in a single location.
    Advantages:
    - Faster model creation, because we don't need to load the NLP each time
    - Better memory efficiency, because we don't have a unique NLP in each session
    """

    def __call__(self, user_input: str):
        return self._nlp(user_input)

    #def ner(self, user_input: str):
    #    return self._ner(user_input)
