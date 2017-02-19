"""Functions and procedures used to draw and interact with the 'Save and exit'
button.
"""

from functools import partial
from typing import Any, Dict, List

from component.write_text import write_centered_text
from gui_parameters import BUTTON_BG_COLOR, BUTTON_FG_COLOR

# Type aliases
ButtonData = Dict[str, Any]
Disk = str
Cylinder = Dict[int, Disk]
Filename = str
Key = List[int]
Letter = str


def generate_exit_button_data(cylinder: Cylinder, key: Key,
                              window) -> ButtonData:
    """Compute the exit button data for later interacting with it. See
    generate_rotation_button_data() for more insight on what button data is.
    """

    button_dimensions = (window.get_width() / 10, window.get_height() / 10)
    button_pos = (window.get_width() - button_dimensions[0],
                  window.get_height() - button_dimensions[1])
    button_surface = window.subsurface(button_pos, button_dimensions)

    return {
        'type': 'exit',
        'surface': button_surface,
        'onclick': partial(write_ciphered_line_to_file, cylinder, key,
                           'encrypted-message.txt'),
        'drawable': True,
        'clickable': True
    }


def draw_exit_button(button_data: ButtonData) -> None:
    """Draw the exit button using its button data."""

    if button_data['drawable']:
        button_surface = button_data['surface']
        button_surface.fill(BUTTON_BG_COLOR)
        write_centered_text(
            'Save and exit',
            button_surface,
            font_size=26,
            font_color=BUTTON_FG_COLOR)


def write_ciphered_line_to_file(cylinder: Cylinder, key: Key, file: Filename):
    """Onto the GUI we can see '< CIPHERED' line. This fonction write this
    precise line of letters into a file with the given filename.
    """

    encrypted_message = ''.join(retrieve_line_from_cylinder(cylinder, key, 15))
    with open(file, 'w') as f:
        f.write(encrypted_message)


def retrieve_line_from_cylinder(cylinder: Cylinder, key: Key,
                                line: int) -> List[Letter]:
    """Return all the <line>th letter of each disk in the cylinder in the order
    given by our secret key.
    """

    return [cylinder[disk_number][line] for disk_number in key]
