"""Functions and procedures used to draw and interact with a rotation button."""

from functools import partial
from typing import Any, Dict, List

import pygame

from component.rotate_disk import rotate_disk_from_cylinder_in_place
from gui_parameters import BUTTON_BG_COLOR, BUTTON_FG_COLOR

# Type aliases
ButtonData = Dict[str, Any]
Disk = str
Cylinder = Dict[int, Disk]
Key = List[int]


def generate_rotation_buttons_data(cylinder: Cylinder, key: Key,
                                   window) -> List[ButtonData]:
    """Compute all of the information needed to draw the rotation buttons and
    later interact with them.
    """

    return flatten([[
        generate_rotation_button_data(cylinder, disk_number, location, True,
                                      window),
        generate_rotation_button_data(cylinder, disk_number, location, False,
                                      window)
    ] for location, disk_number in enumerate(key)])


def generate_rotation_button_data(cylinder: Cylinder,
                                  disk_number: int,
                                  location: int,
                                  does_rotate_up: bool,
                                  window) -> ButtonData:
    """Generate the button data for <disk_number>th disk. The button data
    contains its type (what is this button), its surface to be drawn onto, a
    procedure to call when clicking on it, and two booleans used to know
    whether we can click on it and draw it or not.
    """

    button_dimensions = (window.get_width() / 10 * 9 / len(cylinder),
                         window.get_height() / 10 / 2)
    button_surface_pos = (button_dimensions[0] * location,
                          window.get_height() - button_dimensions[1] *
                          (2 if does_rotate_up else 1))
    button_surface = window.subsurface(button_surface_pos, button_dimensions)

    return {
        'type': 'rotation',
        'does_rotate_up': does_rotate_up,
        'surface': button_surface,
        'onclick': partial(rotate_disk_from_cylinder_in_place, cylinder,
                           disk_number, does_rotate_up),
        'clickable': True,
        'drawable': True
    }


def draw_rotation_buttons(buttons_data: List[ButtonData]) -> None:
    """Draw all the buttons in rotation buttons using all the button data
    inside buttons_data.
    """

    for button_data in buttons_data:
        draw_rotation_button(button_data)


def draw_rotation_button(button_data: ButtonData) -> None:
    """Draw the rotation button according to the button data given. This
    essentially consists into filling the button surface and drawing a little
    arrow onto it.
    """

    if button_data['drawable']:
        button_surface = button_data['surface']

        button_surface.fill(BUTTON_BG_COLOR)

        does_rotate_up = button_data['does_rotate_up']
        left = button_surface.get_rect().left
        right = button_surface.get_rect().right
        top = button_surface.get_rect().top
        bottom = button_surface.get_rect().bottom
        w = (right - left) / 100  # One percent width
        h = (bottom - top) / 100  # One percent height
        point_list = [[
            left + (20 * w), ((bottom - 20 * h)
                              if does_rotate_up else (top + 20 * h))
        ], [
            right / 2, ((top + 20 * h)
                        if does_rotate_up else (bottom - 20 * h))
        ], [
            right - (20 * w), ((bottom - 20 * h)
                               if does_rotate_up else (top + (20 * h)))
        ]]
        pygame.draw.aalines(button_surface, BUTTON_FG_COLOR, False, point_list)


def flatten(l: List[List[Any]]) -> List[Any]:
    """Return a one dimensional list made resulting from the concatenation of
    all the elements of a given two dimensional list."""

    return [x for y in l for x in y]
