"""
Resources:
- https://github.com/commonsense/conceptnet5
- Semantic Association
"""

from typing import Optional, List, Set

from ...database.redis import Event


def get_unique_tags() -> Set[str]:
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
    unique_types = get_unique_tags()

    def __call__(self, tokens: List[str]) -> Optional[List[str]]:
        # Remove the duplicates in the tokens
        # (we don't want to explore the graph twice for the same token)
        tokens = set(tokens)
