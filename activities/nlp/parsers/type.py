"""
Resources:
- https://github.com/commonsense/conceptnet5
- Semantic Association
"""

import pickle

from typing import Optional, Set
from networkx import MultiDiGraph

from ...config import project_root
from ...database.redis import Event


def get_unique_tags() -> Set[str]:
    pks = Event.all_pks()
    tags = set()
    for pk in pks:
        event = Event.get(pk)
        tags.update(event.tags)
    return tags


def load_conceptnet() -> MultiDiGraph:
    file = project_root.parent / 'conceptnet.gpickle'
    if not file.exists():
        print('Could not load ConceptNet graph, launch `pull_data.py`')
        return MultiDiGraph()
    return pickle.load(file.open(mode='rb'))


class TypeParser:
    """
    Parses a user input describing an activity, and returns one or more
    tags matching those in the database.
    """

    # At runtime, collect all the unique types found in the database.
    unique_types = get_unique_tags()
    graph: MultiDiGraph = load_conceptnet()

    def __call__(self, tokens: Set[str]) -> Optional[Set[str]]:
        tags = set()

        for token in tokens:

            if token in self.unique_types:
                tags.update(token)

            if not self.graph.has_node(token):
                # The token is not in the graph, skip
                continue

            related = set(self.graph.successors(token))
            # Keep the intersection between the tags in the database and the
            # successors of the token in the graph
            related_tags = self.unique_types.intersection(related)

            if len(related_tags) == 0:
                continue
            elif len(related_tags) == 1:
                tags.update(related_tags)
            elif len(related_tags) > 1:
                # If there are multiple possibilities for a single token,
                # return the one with the highest weight (if equal, return any)
                weights = {
                    tag: sum([
                        data['weight']
                        for (rel, data) in self.graph.get_edge_data(token, tag).items()
                    ])
                    for tag in related_tags
                }
                # To descending order
                weights = dict(sorted(weights, key=lambda pair: pair[1], reverse=True))
                # Keep the first, which is the one with the highest weight
                tags.update(list(weights.items())[0][0])

        return tags
