"""
This file contains configuration values used throughout the project.
This is the standard client config file (meaning, the one you should use if
you don't use the docker-compose file shipped with the project).
Refer to the file `README.md` in the root directory for more information.
"""

from pathlib import Path
from typing import Dict, Any


project_root: Path = Path(__name__).parent

redis_server_address: str = 'http://localhost'
redis_server_port: int = 6379
redis_server_dbfilename: Path = project_root / 'dump.rdb'
# Additional config parameters passed to the Redis server
# See https://redis-py.readthedocs.io/en/stable/connections.html#redis.Redis
redis_server_config: Dict[str, Any] = {}

model_cookie_name: str = 'model_info'
secret_key_file: Path = project_root / 'secret_key'
