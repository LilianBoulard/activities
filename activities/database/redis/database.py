"""
Implements a Redis database to interact with a server.

Redis resources:
- https://realpython.com/python-redis/
- https://redis.io/commands/
"""

from __future__ import annotations

import redis as rd

from typing import List, Any

Event = Any
#from .models import Event
from ...config import (redis_server_address, redis_server_port,
                       redis_server_dbfilename, redis_server_config)


class RedisDatabase:

    """
    Implements a Redis database to interact with a server.

    Instantiating the database reads the database from disk by default.
    To prevent this behavior, delete the file from disk and/or
    use the `reset` method.
    """

    dbfilename = redis_server_dbfilename

    def __init__(self):
        self._db = rd.Redis(
            host=redis_server_address,
            port=redis_server_port,
            **redis_server_config
        )
        self._db.config_set('dbfilename', str(self.dbfilename))

    def bulk_add(self, events: List[Event]) -> None:
        """
        Bulk-adds multiple events to the Redis database.
        """
        pass

    def add(self, event: Event) -> None:
        """
        Adds a single element to the Redis database.
        """
        pass

    def save(self) -> None:
        """
        Saves the database to the disk.
        """
        self._db.save()

    def is_empty(self) -> bool:
        """
        Checks if the database holds any data.
        Returns True if it does, False otherwise.
        """
        pass

    def reset(self) -> None:
        """
        Empties the database.
        """
        pass
