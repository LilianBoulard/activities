"""
This file contains configuration values used throughout the project.
This is the configuration file meant to be used for deployments on docker.
Refer to both `README.md` and  `docker-compose.yml` in the root directory
for more information.
"""

from pathlib import Path
from typing import Dict, Any
from pytz import timezone as _timezone


project_root: Path = Path(__name__).parent

redis_server_address: str = 'redis.activities_redis_bridge'
redis_server_port: int = 6379
# Additional config parameters passed to the Redis server
# See https://redis-py.readthedocs.io/en/stable/connections.html#redis.Redis
redis_server_config: Dict[str, Any] = {}

secret_key_file: Path = project_root / 'secret_key'

timezone = _timezone('Europe/Paris')
