"""
Resources:
- https://github.com/commonsense/conceptnet5
- Semantic Association
"""

from typing import Optional, List, Set

from ...database.redis import Event


def _get_unique_types() -> Set[str]:
    events = Event.all_pks()
    tags = set()
    for event in events:
        tags.update(event.tags.split(';'))
    return tags


class TypeParser:
    """
    Parses a user input describing an activity, and returns one or more
    tags matching those in the database.
    """

    # At runtime, collect all the unique types found in the database.
    #unique_types = _get_unique_types()

    def __call__(self, user_input: str) -> Optional[List[str]]:
        pass
