import os
import json

from .config import secret_key_file, redis_conf_file

from typing import List, Tuple, Dict
from collections import defaultdict


def get_redis_password():
    """
    Reads the redis config and returns the password.
    """
    if redis_conf_file.is_file():
        with redis_conf_file.open('r') as fl:
            for line in fl.readlines():
                if line.startswith('requirepass'):
                    _, password = line.split()
                    return password
            else:
                raise ValueError(f'Could not find a "requirepass" statement '
                                 f'in the config file {redis_conf_file}')
    else:
        raise FileNotFoundError(
            f'Redis config file could not be found at {redis_conf_file!s} '
            f'please modify it in the config if you are not using docker, '
            f'otherwise, check the compose file. '
        )


def secret_key() -> bytes:
    """
    Gets a secret key, either from reading an already existing file,
    or by creating a new one (and writing it to disk).
    """
    if secret_key_file.is_file():
        with secret_key_file.open(mode='rb') as fl:
            key = fl.read()
    else:
        key = os.urandom(24)
        with secret_key_file.open(mode='wb') as fl:
            fl.write(key)
    return key


def encode_json(dictionary: dict) -> str:
    """
    Takes a dictionary and returns a JSON-encoded string.
    """
    return json.JSONEncoder().encode(dictionary)


def decode_json(json_string: str) -> dict:
    """
    Takes a message as a JSON string and unpacks it to get a dictionary.
    """
    return json.JSONDecoder().decode(json_string)


def zip_to_dict(items: List[Tuple[str, str]]) -> Dict[str, List[str]]:
    """
    Converts a zip (a list of 2-tuples) to a dictionary representation
    by using the first field as the value and the second as the key.

    Example:
        >>> zip_to_dict([("Google", "ORG"), ("NASA", "GOV"), ("FBI", "GOV")])
        {"ORG": ["Google"], "GOV": ["NASA", "FBI"]}
    """
    final = defaultdict()
    for key, value in items:
        final[key].append(value)
    return dict(final)
