from random import sample
from string import ascii_letters, ascii_uppercase
from typing import Dict, List

# Type aliases
Filename = str
Cylinder = str
Key = List[int]


def sanitize_message(message: str) -> str:
    """Given a message, will discard all characters not being alphabetic."""

    return ''.join(
        filter(lambda character: character in ascii_letters, message))


def generate_cylinder() -> Cylinder:
    """Return all letters of the alphabet uppercase in a random order as a
    string, i.e. a cylinder.
    """

    return ''.join(sample(ascii_uppercase, 26))


def write_cylinders_to_file(file: Filename, number_of_cylinders: int) -> None:
    """Write to file a given number of shuffled alphabets (cylinders), with one
    alphabet per line.
    """

    f = open(file, 'w')
    for _ in range(number_of_cylinders):
        f.write(generate_cylinder() + '\n')
    f.close()


def load_cylinders_from_file(file: Filename) -> Dict[int, Cylinder]:
    """Read file line by line and return a dict composed of the content of each
    line as values and their line number as keys.
    """

    f = open(file, 'r')
    raw_cylinders = f.read()
    f.close()
    return {
        i + 1: cylinder
        for i, cylinder in enumerate(raw_cylinders.split('\n'))
        if cylinder is not ''  # Exclude last empty line
    }


def is_key_valid(key: Key, n: int) -> bool:
    """Check if key is valid, i.e. key is a permutation of all numbers from 1
    to the number of cylinders (included) wanted.
    """

    return sorted(key) == list(range(1, n + 1))


def generate_key(n: int) -> Key:
    """Return a permutation of all number from 1 to n (included)."""

    return sample(list(range(1, n + 1)), n)
