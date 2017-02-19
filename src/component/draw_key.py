"""Procedure used to draw our key."""

from typing import Dict, List

from component.write_text import write_centered_text

# Type aliases
Disk = str
Cylinder = Dict[int, Disk]
Key = List[int]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def draw_key(cylinder: Cylinder, key: Key, window):
    """Draw our not-yet-complete-key below the key selection buttons."""

    for index, number in enumerate(key):
        number_dimensions = (window.get_width() / 10 * 9 / len(cylinder),
                             window.get_height() / 10 / 2)
        number_pos = (number_dimensions[0] * index,
                      window.get_height() - number_dimensions[1])
        number_surface = window.subsurface(number_pos, number_dimensions)
        number_surface.fill(WHITE)
        write_centered_text(str(number), number_surface, font_color=BLACK)
