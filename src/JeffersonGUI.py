"""The Jefferson Graphical Interface. It first load the cylinder from the
'cylinder.txt' file in the current working directory, then the user is prompt
to enter a key to rearrange the disks into its deisred order. Afterwards the
user rotates each disks to display the message he later wants to encrypt on the
'< CLEAR' line.
When done, clicking on 'Save and exit' write the message on the '< CIPHERED'
line to a file named 'encrypted-message.txt' in the current working directory.
"""

import pygame
from pygame.locals import *

from component.draw_cylinder import draw_cylinder
from component.draw_key import draw_key
from component.enter_key_annotation import draw_enter_key_annotation
from component.exit_button import draw_exit_button, generate_exit_button_data
from component.key_selection import (draw_key_selection_buttons,
                                     generate_key_selection_buttons_data)
from component.rotation_button import (draw_rotation_buttons,
                                       generate_rotation_buttons_data)
from component.sidebar_annotation import draw_sidebar_annotation
from gui_parameters import FPS, WINDOW_CAPTION, WINDOW_DIMENSIONS
from JeffersonShell import is_key_valid, load_cylinder_from_file

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# GUI globals
CLOCK = None
CYLINDER = None
EXIT_BUTTON_DATA = None
KEY = None
ROTATION_BUTTONS_DATA = None
WINDOW = None


def main() -> None:
    """Takes care of calling the setup and setting off the drawing loop."""

    setup()
    pass_to_next_frame = True
    while pass_to_next_frame:
        pass_to_next_frame = draw()


def setup() -> None:
    """Initialize pygame and the various GUI globals."""

    global CLOCK
    global CYLINDER
    global EXIT_BUTTON_DATA
    global KEY
    global KEY_SELECTION_BUTTONS_DATA
    global ROTATION_BUTTONS_DATA
    global WINDOW

    pygame.init()

    WINDOW = pygame.display.set_mode(WINDOW_DIMENSIONS)
    pygame.display.set_caption(WINDOW_CAPTION)

    CLOCK = pygame.time.Clock()

    CYLINDER = load_cylinder_from_file('cylinder.txt')

    KEY = []

    ROTATION_BUTTONS_DATA = generate_rotation_buttons_data(
        CYLINDER, list(range(1, len(CYLINDER) + 1)), WINDOW)
    KEY_SELECTION_BUTTONS_DATA = generate_key_selection_buttons_data(CYLINDER,
                                                                     WINDOW)
    EXIT_BUTTON_DATA = generate_exit_button_data(CYLINDER, KEY, WINDOW)


def draw() -> bool:
    """Main drawing procedure, it calls all of the others drawing
    subroutines. If the program must terminates, this subroutine will return
    False to exit the drawing loop.
    """

    global EXIT_BUTTON_DATA
    global KEY
    global KEY_SELECTION_BUTTONS_DATA
    global ROTATION_BUTTONS_DATA

    key_valid = is_key_valid(KEY, len(CYLINDER))
    ROTATION_BUTTONS_DATA = generate_rotation_buttons_data(
        CYLINDER, KEY
        if key_valid else list(range(1, len(CYLINDER) + 1)), WINDOW)

    # Redraw UI
    clear_surface(WINDOW)
    draw_cylinder(CYLINDER, KEY
                  if key_valid else list(range(1, len(CYLINDER) + 1)), WINDOW)
    draw_sidebar_annotation("< CLEAR", 9, WINDOW)
    draw_sidebar_annotation("< CIPHERED", 15, WINDOW)
    if key_valid:
        draw_rotation_buttons(ROTATION_BUTTONS_DATA)
        draw_exit_button(EXIT_BUTTON_DATA)
    else:
        draw_key_selection_buttons(KEY_SELECTION_BUTTONS_DATA)
        draw_key(CYLINDER, KEY, WINDOW)
        draw_enter_key_annotation(WINDOW)
    pygame.display.flip()

    # Compute if we can click on the rotation button and finish button
    for button in ROTATION_BUTTONS_DATA:
        button['clickable'] = key_valid
    EXIT_BUTTON_DATA['clickable'] = key_valid

    # Compute the UI components we can interact onto for this frame
    clickable_components = [
        component
        for component in ROTATION_BUTTONS_DATA + KEY_SELECTION_BUTTONS_DATA +
        [EXIT_BUTTON_DATA] if component['clickable']
    ]

    # Handle events
    for event in pygame.event.get():
        if event.type is QUIT:
            return False  # Abort program
        elif event.type is MOUSEBUTTONUP:
            for clickable_component in clickable_components:
                abs_component_rect = pygame.Rect(
                    clickable_component['surface'].get_abs_offset(),
                    clickable_component['surface'].get_size())

                if (abs_component_rect.collidepoint(event.pos)):
                    clickable_component['onclick']()

                    if clickable_component['type'] == 'key_selection':
                        KEY.append(clickable_component['disk_number'])
                    elif clickable_component['type'] == 'exit':
                        return False  # We clicked 'Save and exit', exit the
                        # program

                    # Wait the end of the frame
    CLOCK.tick(FPS)
    return True


def clear_surface(surface) -> None:
    """Fill surface with black."""

    surface.fill(BLACK)


if __name__ == "__main__":
    main()
