"""
This script is to be executed manually on the host machine right after
the repository has been cloned.
"""

from hashlib import md5
from pathlib import Path
from random import choice
from string import ascii_letters, digits


if __name__ == "__main__":
    directory = Path(__file__).parent  # The current file's dir
    mysql_root_password_file = directory / 'secret_mysql_root_password'
    mysql_password_file = directory / 'secret_mysql_password'
    redis_password_file = directory / 'redis.conf'

    characters = ascii_letters + digits

    # Yes, I know, it's pseudo-random.
    mysql_root_password = md5((choice(characters) * 16).encode('utf8')).hexdigest()[:16]
    mysql_password = md5((choice(characters) * 16).encode('utf8')).hexdigest()[:16]
    redis_password = md5((choice(characters) * 16).encode('utf8')).hexdigest()[:16]

    if not mysql_root_password_file.is_file():
        with mysql_root_password_file.open('w') as fl:
            fl.write(mysql_root_password)
            print(f'Wrote random password in {mysql_root_password_file}')
    else:
        print(f'Ignoring {mysql_root_password_file!s} as it already exists')

    if not mysql_password_file.is_file():
        with mysql_password_file.open('w') as fl:
            fl.write(mysql_password)
            print(f'Wrote random password in {mysql_password_file}')
    else:
        print(f'Ignoring {mysql_password_file!s} as it already exists')

    if not redis_password_file.is_file():
        with redis_password_file.open('w') as fl:
            fl.write(f'requirepass {redis_password}')
            print(f'Wrote random password in {redis_password_file}')
    else:
        print(f'Ignoring {redis_password_file!s} as it already exists')
