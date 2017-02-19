"""Functions and procedures used to draw the key selection prompt."""

from functools import partial
from typing import Any, Dict, List

from component.write_text import write_centered_text
from gui_parameters import BUTTON_BG_COLOR, BUTTON_FG_COLOR

# Type aliases
ButtonData = Dict['str', Any]
Disk = str
Cylinder = Dict[int, Disk]


def generate_key_selection_buttons_data(cylinder: Cylinder,
                                        window) -> List[ButtonData]:
    """Compute the button data for every key selection buttons."""

    return [
        generate_key_selection_button_data(cylinder, disk_number, window)
        for disk_number in range(1, len(cylinder) + 1)
    ]


def generate_key_selection_button_data(cylinder: Cylinder,
                                       disk_number: int,
                                       window) -> ButtonData:
    """Return the button data of a key selection button, the ones we use to
    select the key at the program's startup. See
    generate_rotation_button_data() for more insight on what a ButtonData
    contains.
    """

    button_dimensions = (window.get_width() / 10 * 9 / len(cylinder),
                         window.get_height() / 10 / 2)
    button_pos = (button_dimensions[0] * (disk_number - 1),
                  window.get_height() - button_dimensions[1] * 2)
    button_surface = window.subsurface(button_pos, button_dimensions)

    button_data = {
        'type': 'key_selection',
        'disk_number': disk_number,
        'surface': button_surface,
        'onclick': None,
        'clickable': True,
        'drawable': True
    }

    def onclick(button_data: ButtonData):
        """Disable the button once we clicked on it."""

        button_data['clickable'] = False
        button_data['drawable'] = False

    button_data['onclick'] = partial(onclick, button_data)

    return button_data


def draw_key_selection_buttons(buttons_data: List[ButtonData]) -> None:
    """Draw all the key selection buttons."""

    for button_data in buttons_data:
        draw_key_selection_button(button_data)


def draw_key_selection_button(button_data: ButtonData) -> None:
    """Draw a key selection button using the button data given."""

    if button_data['drawable']:
        button_surface = button_data['surface']
        button_surface.fill(BUTTON_BG_COLOR)
        write_centered_text(
            str(button_data['disk_number']),
            button_surface,
            font_color=BUTTON_FG_COLOR)
