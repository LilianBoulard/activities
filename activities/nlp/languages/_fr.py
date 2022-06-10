from ._base import NLP, load_nlp
from ...design import Singleton, apply_init_callback_to_singleton


@apply_init_callback_to_singleton(lambda instance: load_nlp(instance, 'fr_dep_news_trf'))
class FRNLP(NLP, Singleton):
    """
    This subclass is a placeholder.
    It's empty, and that's normal :)
    """
    pass
