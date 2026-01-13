import argparse
import datetime
import json
import logging
import secrets
import string
from pathlib import Path
from typing import Dict, List, Optional

import geonamescache
import yaml


# ---------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------
def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            'Generate a random profile using curated fictional character names. '
            'You may use your own character list if desired.'
        )
    )

    parser.add_argument(
        '--names',
        default='anime_characters.yaml',
        help='Path to YAML file containing character names'
    )

    parser.add_argument(
        '--username-length',
        type=int,
        default=10,
        help='Username length'
    )

    parser.add_argument(
        '--with-password',
        action='store_true',
        help='Generate a random password'
    )

    parser.add_argument(
        '--password-length',
        type=int,
        help='Password length (requires --with-password)'
    )

    parser.add_argument(
        '--no-password-symbols',
        dest='password_symbols',
        action='store_false',
        help='Disable symbols in generated password'
    )
    parser.set_defaults(password_symbols=True)

    parser.add_argument(
        '--show-password',
        action='store_true',
        help='Display generated password in output'
    )

    parser.add_argument(
        '--save',
        help='Output file path to save the generated profile'
    )

    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        help='Output data format (requires --save)'
    )

    parser.add_argument(
        '--country',
        help='Specify a country name; otherwise, a random country is selected'
    )

    args = parser.parse_args()

    # Infer format from filename
    if args.save and not args.format:
        suffix = Path(args.save).suffix.lower()
        if suffix == '.json':
            args.format = 'json'
        elif suffix == '.txt':
            args.format = 'text'

    # Enforce dependencies
    if args.format and not args.save:
        parser.error('--format requires --save')

    if args.password_length and not args.with_password:
        parser.error('--password-length requires --with-password')

    return args


# ---------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------
def get_random_character(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        data: Dict[str, List[str]] = yaml.safe_load(file)

    if not isinstance(data, dict) or not data:
        raise ValueError('Invalid or empty character file')

    title = secrets.choice(list(data.keys()))
    characters = data.get(title)

    if not characters:
        raise ValueError('Character list is empty')

    return secrets.choice(characters)


def generate_username(length: int) -> str:
    if length < 1:
        raise ValueError('Username length must be positive')

    chars = string.ascii_letters + string.digits
    return secrets.choice(string.ascii_letters) + ''.join(
        secrets.choice(chars) for _ in range(length - 1)
    )


def generate_password(length: int , with_symbols: bool = True) -> str:
    if length < 4:
        raise ValueError('Password length must be at least 4')

    symbols = "!@#$%^&*()-_=+[]{};:,.<>?/|"
    safe_symbols = "-_+*@&%"

    password_chars = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(symbols if with_symbols else safe_symbols),
    ]

    charset = string.ascii_letters + string.digits
    charset += symbols if with_symbols else safe_symbols

    password_chars.extend(
        secrets.choice(charset) for _ in range(length - 4)
    )

    secrets.SystemRandom().shuffle(password_chars)
    return ''.join(password_chars)


def generate_birthdate() -> List[int]:
    year = secrets.randbelow(2010 - 1962 + 1) + 1962
    month = secrets.randbelow(12) + 1
    day = secrets.randbelow(28) + 1
    return [day, month, year]


def get_random_country() -> str:
    countries = geonamescache.GeonamesCache().get_countries_by_names()
    return secrets.choice(list(countries.keys()))


def get_random_city(country_name: str) -> Optional[str]:
    geo = geonamescache.GeonamesCache()
    countries = geo.get_countries_by_names()
    info = countries.get(country_name.capitalize())

    if not info:
        logger.error('Unknown country: %s', country_name)
        return None

    country_code = info['iso']
    cities = [
        city['name']
        for city in geo.get_cities().values()
        if city['countrycode'] == country_code
    ]

    return secrets.choice(cities) if cities else None


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
if __name__ == '__main__':
    args = parse_arguments()

    # Name
    if Path(args.names).is_file():
        try:
            name = get_random_character(args.names)
        except Exception as exc:
            logger.warning('Failed to load names: %s', exc)
            name = ''.join(secrets.choice(string.ascii_letters) for _ in range(8))
    else:
        logger.warning('Name file not found, using random name')
        name = ''.join(secrets.choice(string.ascii_letters) for _ in range(8))

    # Core data
    username = generate_username(args.username_length)
    birth_day, birth_month, birth_year = generate_birthdate()
    age = datetime.date.today().year - birth_year
    country = args.country if args.country else get_random_country()
    city = get_random_city(country)

    password = (
        generate_password(
            args.password_length if args.password_length else 64 ,
            with_symbols=args.password_symbols
        )
        if args.with_password
        else None
    )

    # Output (stdout)
    print(f'name: {name}')
    print(f'username: {username}')
    print(f'date of birth: {birth_day}/{birth_month}/{birth_year}')
    print(f'age: {age}')
    print(f'country: {country}')
    print(f'city: {city}')

    if password:
        if args.show_password:
            print(f'password: {password}')
        else:
            print('password: [hidden]')

    # Save
    if args.save:
        profile = {
            'name': name,
            'username': username,
            'birthdate': f'{birth_day}/{birth_month}/{birth_year}',
            'age': age,
            'country': country,
            'city': city,
        }

        if password:
            profile['password'] = password

        with open(args.save, 'w', encoding='utf-8') as file:
            if args.format == 'json':
                json.dump(profile, file, indent=2)
            else:
                for key, value in profile.items():
                    file.write(f'{key}: {value}\n')

        logger.info('Profile saved to %s', args.save)
