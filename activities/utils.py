import os
import json

from .config import secret_key_file


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
