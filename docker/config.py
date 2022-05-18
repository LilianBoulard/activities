"""
This file contains configuration values used throughout the project.
This is the configuration file meant to be used for deployments on docker.
Refer to both `README.md` and  `docker-compose.yml` in the root directory
for more information.
"""

from pathlib import Path
from typing import Dict, Any


redis_server_address: str = 'http://localhost'
redis_server_port: int = 6379
redis_server_dbfilename: Path = Path(__file__).parent / 'dump.rdb'
# Additional config parameters passed to the Redis server
# See https://redis-py.readthedocs.io/en/stable/connections.html#redis.Redis
redis_server_config: Dict[str, Any] = {}
