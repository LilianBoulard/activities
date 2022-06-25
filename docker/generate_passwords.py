"""
This script is to be executed manually on the host machine right after
the repository has been cloned.
"""

from hashlib import md5
from pathlib import Path
from random import choice
from string import ascii_letters, digits


characters = ascii_letters + digits


def generate_pass(n: int = 16):
    # Yes, I know, it's pseudo-random.
    return md5((choice(characters) * n).encode('utf8')).hexdigest()[:n]


if __name__ == "__main__":
    directory = Path(__file__).parent  # The current file's dir
    env_file = directory / 'stack.env'

    if not env_file.is_file():
        with env_file.open('w') as fl:
            fl.write(f'MYSQL_ROOT_PASSWORD={generate_pass()}\n')
            fl.write(f'MYSQL_PASSWORD={generate_pass()}\n')
            fl.write(f'REDIS_PASSWORD={generate_pass()}\n')
            print(f'Wrote random passwords in {env_file}')
    else:
        print(f'Ignoring {env_file!s} as it already exists')
