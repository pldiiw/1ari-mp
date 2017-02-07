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

    with open(file, 'w') as f:
        for _ in range(number_of_cylinders):
            f.write(generate_cylinder() + '\n')


def load_cylinders_from_file(file: Filename) -> Dict[int, Cylinder]:
    """Read file line by line and return a dict composed of the content of each
    line as values and their line number as keys.
    """

    with open(file, 'r') as f:
        raw_cylinders = f.read()
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


def find(letter: str, cylinder: Cylinder) -> int:
    """Return the index of the first occurence of letter in cylinder. It
    returns -1 if there is no occurence of letter.
    """

    occurs_at = -1
    for i, v in enumerate(cylinder):
        if occurs_at is -1 and v == letter:
            occurs_at = i
            break
    return occurs_at


def shift(n: int, add: int, mod: int) -> int:
    """Shift n of add modulo mod."""

    return (n + add) % mod


def jefferson_shift(n: int) -> int:
    """Shift n of 6 modulo 26. Partial application of shift."""

    return shift(n, 6, 26)
