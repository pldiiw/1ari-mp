"""Procedures to draw a cylinder onto the screen."""

from typing import Dict, List

from component.write_text import write_centered_text

# Type aliases
Disk = str
Cylinder = Dict[int, Disk]
Letter = str
Key = List[int]


def draw_cylinder(cylinder: Cylinder, key: Key, window) -> None:
    """Given a cylinder, it will draw every disks the cylinder contains onto
    the surface where the cylinder is ought to be drawn (cylinder_surface) in
    the order given by our secret key.
    """

    cylinder_dimensions = (window.get_width() / 10 * 9,
                           window.get_height() / 10 * 9)
    cylinder_pos = (0, 0)
    cylinder_surface = window.subsurface(cylinder_pos, cylinder_dimensions)

    for location, disk_number in enumerate(key):
        draw_disk(cylinder, disk_number, location, cylinder_surface)


def draw_disk(cylinder: Cylinder,
              disk_number: int,
              location: int,
              cylinder_surface) -> None:
    """Draw a disk at the given location where it should be drawn onto the
    cylinder_surface.
    """

    disk_dimensions = (cylinder_surface.get_width() / len(cylinder),
                       cylinder_surface.get_height())
    disk_pos = (disk_dimensions[0] * location, 0)
    disk_surface = cylinder_surface.subsurface(disk_pos, disk_dimensions)

    for letter_number, letter in enumerate(cylinder[disk_number]):
        draw_letter(letter, letter_number, disk_surface)


def draw_letter(letter: Letter, letter_number: int, disk_surface) -> None:
    """Draw a letter at the index provided onto the disk surface."""

    letter_dimensions = (disk_surface.get_width(),
                         disk_surface.get_height() / 26)
    letter_pos = (0, letter_dimensions[1] * letter_number)
    letter_surface = disk_surface.subsurface(letter_pos, letter_dimensions)
    write_centered_text(letter, letter_surface)
