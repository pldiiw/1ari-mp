from random import sample
from string import ascii_letters, ascii_uppercase
from typing import Dict, List

# Type aliases
Filename = str
Disk = str
Cylinder = Dict[int, Disk]
Key = List[int]
Letter = str


def sanitize_message(message: str) -> str:
    """Given a message, will discard all characters not being alphabetic."""

    return ''.join(
        filter(lambda character: character in ascii_letters, message))


def generate_disk() -> Disk:
    """Return all letters of the alphabet uppercase in a random order as a
    string, i.e. a Jefferson disk.
    """

    return ''.join(sample(ascii_uppercase, 26))


def write_cylinder_to_file(file: Filename, number_of_disks: int) -> None:
    """Write to file a given number of shuffled alphabets (disks), with one
    alphabet per line.
    """

    with open(file, 'w') as f:
        for _ in range(number_of_disks):
            f.write(generate_disk() + '\n')


def load_cylinder_from_file(file: Filename) -> Cylinder:
    """Read file line by line and return a dict composed of the content of each
    line as values and their line number as keys.
    """

    with open(file, 'r') as f:
        raw_cylinder = f.read()
        return {
            i + 1: disk
            for i, disk in enumerate(raw_cylinder.split('\n'))
            if disk is not ''  # Exclude last empty line
        }


def is_key_valid(key: Key, n: int) -> bool:
    """Check if key is valid, i.e. key is a permutation of all numbers from 1
    to the number of disks (included) wanted.
    """

    return sorted(key) == list(range(1, n + 1))


def generate_key(n: int) -> Key:
    """Return a permutation of all number from 1 to n (included)."""

    return sample(list(range(1, n + 1)), n)


def find(letter: Letter, disk: Disk) -> int:
    """Return the index of the first occurence of letter in disk. It
    returns -1 if there is no occurence of letter.
    """

    occurs_at = -1
    for i, v in enumerate(disk):
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


def revert_jefferson_shift(n: int) -> int:
    """Shift n of 6 modulo 26. Partial application of shift."""

    return shift(n, -6, 26)


def cipher_letter(letter: Letter, disk: Disk) -> Letter:
    """Encrypt letter using the jefferson disk provided."""

    return disk[jefferson_shift(find(letter, disk))]


def decipher_letter(letter: Letter, disk: Disk) -> Letter:
    """Decrypt letter using the jefferson disk provided."""

    return disk[revert_jefferson_shift(find(letter, disk))]


def cipher_message(message: str, key: Key, cylinder: Cylinder) -> str:
    """Encrypt message with the Jefferson method using the key and the set of
    disks provided.
    """

    if is_key_valid(key, len(key)):
        return ''.join([
            cipher_letter(letter, cylinder[key[index]])
            for index, letter in enumerate(message)
        ])
    else:
        raise Exception("The key provided is not valid.")


def decipher_message(message: str, key: Key, cylinder: Cylinder) -> str:
    """Decrypt message with the Jefferson method using the key and the set of
    disks provided.
    """

    if is_key_valid(key, len(key)):
        return ''.join([
            decipher_letter(letter, cylinder[key[index]])
            for index, letter in enumerate(message)
        ])
    else:
        raise Exception("The key provided is not valid.")
