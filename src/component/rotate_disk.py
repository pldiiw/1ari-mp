"""Functions and procedures used to rotate a disk."""

from typing import Dict, List

# Type aliases
Disk = str
Cylinder = Dict[int, Disk]


def rotate_disk_from_cylinder_in_place(cylinder: Cylinder,
                                       disk_number: int,
                                       does_rotate_up: bool=True) -> None:
    """Rotate a disk from the given cylinder in place."""

    cylinder[disk_number] = rotate_disk(cylinder[disk_number], does_rotate_up)


def rotate_disk(disk: Disk, does_rotate_up: bool=True) -> Disk:
    """Shift all elements of disk by one."""

    return ''.join(shift_list(list(disk), -1 if does_rotate_up else 1))


def shift_list(l: List, n: int) -> List:
    """Return a new list based on the one given with its elements shifted n
    times.
    """

    return [l[(i - n) % len(l)] for i in range(len(l))]
