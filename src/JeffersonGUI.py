from functools import partial
from string import ascii_uppercase
from typing import Any, Callable, Dict, List, Tuple

import pygame
from pygame.locals import *

# Type aliases
Disk = str
Cylinder = Dict[int, Disk]
Key = List[int]
Letter = str
ButtonData = Dict[str, Any]
Color = Tuple[int, int, int]

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# GUI Parameters
FPS = 30
WINDOW_DIMENSIONS = (1500, 1000)  # (width, heigth)
WINDOW_CAPTION = 'Jefferson Disk'
FONT_NAME = 'FixedSys'
FONT_SIZE = 32
FONT_COLOR = WHITE
BUTTON_FG_COLOR = BLACK
BUTTON_BG_COLOR = WHITE

# GUI globals
CLOCK = None
CYLINDER = None
FINISH_BUTTON_DATA = None
KEY = None
ROTATION_BUTTONS_DATA = None
VALIDATE_KEY_BUTTON_DATA = None
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
    global FINISH_BUTTON_DATA
    global KEY
    global KEY_SELECTION_BUTTONS_DATA
    global ROTATION_BUTTONS_DATA
    global VALIDATE_KEY_BUTTON_DATA
    global WINDOW

    pygame.init()

    WINDOW = pygame.display.set_mode(WINDOW_DIMENSIONS)
    pygame.display.set_caption(WINDOW_CAPTION)

    CLOCK = pygame.time.Clock()

    CYLINDER = {i: ascii_uppercase for i in range(1, 11)}

    ROTATION_BUTTONS_DATA = generate_rotation_buttons_data(CYLINDER, WINDOW)
    KEY_SELECTION_BUTTONS_DATA = generate_key_selection_buttons_data(CYLINDER,
                                                                     WINDOW)
    FINISH_BUTTON_DATA = generate_finish_button_data(WINDOW)
    VALIDATE_KEY_BUTTON_DATA = generate_validate_key_button_data(WINDOW)

    KEY = []


def draw() -> bool:
    """Main drawing procedure, it calls all of the others drawing
    subroutines. If the program must terminates, this subroutine will return
    False to exit the drawing loop.
    """

    global FINISH_BUTTON_DATA
    global KEY
    global KEY_SELECTION_BUTTONS_DATA
    global ROTATION_BUTTONS_DATA
    global VALIDATE_KEY_BUTTON_DATA

    can_be_drawn_and_clickable = (not VALIDATE_KEY_BUTTON_DATA['clickable'])
    # Redraw UI
    clear_surface(WINDOW)
    draw_cylinder(CYLINDER, WINDOW)
    draw_rotation_buttons(ROTATION_BUTTONS_DATA)
    draw_sidebar_annotation("< CLEAR", 9, WINDOW)
    draw_sidebar_annotation("< CIPHERED", 15, WINDOW)
    draw_finish_button(FINISH_BUTTON_DATA)
    draw_validate_key_button(VALIDATE_KEY_BUTTON_DATA)
    draw_key_selection_buttons(KEY_SELECTION_BUTTONS_DATA)
    if not can_be_drawn_and_clickable:
        draw_key(CYLINDER, KEY, WINDOW)
    pygame.display.flip()

    # Compute what's drawable and what's not for the next frame
    for button in ROTATION_BUTTONS_DATA:
        button['drawable'] = can_be_drawn_and_clickable
        button['clickable'] = can_be_drawn_and_clickable
    if can_be_drawn_and_clickable:
        for button in KEY_SELECTION_BUTTONS_DATA:
            button['drawable'] = not can_be_drawn_and_clickable
            button['clickable'] = not can_be_drawn_and_clickable
    FINISH_BUTTON_DATA['drawable'] = can_be_drawn_and_clickable
    FINISH_BUTTON_DATA['clickable'] = can_be_drawn_and_clickable

    # Compute the UI components we can interact onto for this frame
    clickable_components = [
        component
        for component in ROTATION_BUTTONS_DATA + KEY_SELECTION_BUTTONS_DATA
        + [FINISH_BUTTON_DATA, VALIDATE_KEY_BUTTON_DATA]
        if component['clickable']
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
                        print(KEY)

    # Wait the end of the frame
    CLOCK.tick(FPS)
    return True


def draw_cylinder(cylinder: Cylinder, window) -> None:
    """Given a cylinder, it will draw every disks the cylinder contains onto
    the surface where the cylinder is ought to be drawn (CYLINDER_SURFACE).
    """

    cylinder_dimensions = (window.get_width() / 10 * 9,
                           window.get_height() / 10 * 9)
    cylinder_pos = (0, 0)
    cylinder_surface = window.subsurface(cylinder_pos, cylinder_dimensions)

    for disk_number in cylinder:
        draw_disk(cylinder, disk_number, cylinder_surface)


def draw_disk(cylinder: Cylinder, disk_number: int, cylinder_surface) -> None:
    """Given a disk, its position on the cylinder and a surface to draw on,
    this subroutine will draw this disk at the appropriate location.
    """

    disk_dimensions = (cylinder_surface.get_width() / len(cylinder),
                       cylinder_surface.get_height())
    disk_pos = (disk_dimensions[0] * (disk_number - 1), 0)
    disk_rect = pygame.Rect(disk_pos, disk_dimensions)
    disk_surface = cylinder_surface.subsurface(disk_rect)

    for letter_number, letter in enumerate(cylinder[disk_number]):
        draw_letter(letter, letter_number, disk_surface)


def draw_letter(letter: Letter, letter_number: int, disk_surface) -> None:
    """Draw a letter at the index provided onto the disk surface."""

    letter_dimensions = (disk_surface.get_width(),
                         disk_surface.get_height() / 26)
    letter_pos = (0, letter_dimensions[1] * letter_number)
    letter_rect = pygame.Rect(letter_pos, letter_dimensions)
    letter_surface = disk_surface.subsurface(letter_rect)
    write_centered_text(letter, letter_surface)


def write_centered_text(text: str,
                        parent_surface,
                        font_size: int=FONT_SIZE,
                        font_color: Color=FONT_COLOR) -> None:
    """Draw text centered onto the parent surface given."""

    font = pygame.font.Font(pygame.font.match_font(FONT_NAME), font_size)
    text_surface = font.render(text, True, font_color)
    text_pos = text_surface.get_rect(center=(
        0.5 * parent_surface.get_width(), 0.5 * parent_surface.get_height()))
    parent_surface.blit(text_surface, text_pos)


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


def generate_rotation_buttons_data(cylinder: Cylinder,
                                   window) -> List[ButtonData]:
    """Compute all of the information needed to draw the rotation buttons and
    later interact with them.
    """

    return flatten([[
        generate_rotation_button_data(cylinder, disk_number, True, window),
        generate_rotation_button_data(cylinder, disk_number, False, window)
    ] for disk_number in range(1, len(cylinder) + 1)])


def generate_rotation_button_data(cylinder: Cylinder,
                                  disk_number: int,
                                  does_rotate_up: bool,
                                  window) -> ButtonData:
    """Generate rotation button data for disk disk_number."""

    button_dimensions = (window.get_width() / 10 * 9 / len(cylinder),
                         window.get_height() / 10 / 2)
    button_surface_pos = (button_dimensions[0] * (disk_number - 1),
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
    """Draw all the buttons in rotation buttons inside buttons_data."""

    for button_data in buttons_data:
        draw_rotation_button(button_data)


def draw_rotation_button(button_data: ButtonData) -> None:
    """Draw the rotation button according to the button data given. This
    essentially consists into filling the button surface and drawing a little
    arrow onto it.
    """

    button_surface = button_data['surface']
    if button_data['drawable']:
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


def generate_finish_button_data(window) -> ButtonData:
    """Create a dict for later interacting with the finish button."""

    button_dimensions = (window.get_width() / 10, window.get_height() / 10)
    button_pos = (window.get_width() - button_dimensions[0],
                  window.get_height() - button_dimensions[1])
    button_surface = window.subsurface(button_pos, button_dimensions)

    return {
        'type': 'finish',
        'surface': button_surface,
        'onclick': partial(print, 'FINISH'),  # TODO
        'drawable': True,
        'clickable': True
    }


def draw_finish_button(button_data: ButtonData) -> None:
    """Draw the finish button using its button data."""

    button_surface = button_data['surface']
    if button_data['drawable']:
        button_surface.fill(BUTTON_BG_COLOR)
        write_centered_text(
            'Finish', button_surface, font_color=BUTTON_FG_COLOR)


def draw_sidebar_annotation(text: str, column_number: int, window) -> None:
    """Draw an annotated text onto the sidebar at the given column, relative to
    the ones of the disks."""

    annotation_dimensions = (window.get_width() / 10,
                             (window.get_height() / 10 * 9) / 26)
    annotation_pos = (window.get_width() - annotation_dimensions[0],
                      annotation_dimensions[1] * column_number)
    annotation_surface = window.subsurface(annotation_pos,
                                           annotation_dimensions)
    write_left_aligned_text(text, annotation_surface)


def write_left_aligned_text(text: str,
                            parent_surface,
                            font_size: int=FONT_SIZE,
                            font_color: Color=FONT_COLOR) -> None:
    """Write the given text at the left border of the parent surface."""

    font = pygame.font.Font(pygame.font.match_font(FONT_NAME), font_size)
    text_surface = font.render(text, True, font_color)
    text_pos = text_surface.get_rect(center=(
        0.5 * parent_surface.get_width(), 0.5 * parent_surface.get_height()))
    text_pos.left = 0  # Align text with left border
    parent_surface.blit(text_surface, text_pos)


def generate_validate_key_button_data(window) -> ButtonData:
    """Get the 'Validate key' button data."""

    button_dimensions = (window.get_width() / 10, window.get_height() / 10)
    button_pos = (window.get_width() - button_dimensions[0],
                  window.get_height() - button_dimensions[1])
    button_surface = window.subsurface(button_pos, button_dimensions)

    button_data = {
        'type': 'validate_key',
        'surface': button_surface,
        'onclick': None,
        'drawable': True,
        'clickable': True
    }

    def onclick(button_data: ButtonData) -> None:  # TODO: Not complete
        button_data['clickable'] = False
        button_data['drawable'] = False

    button_data['onclick'] = partial(onclick, button_data)

    return button_data


def draw_validate_key_button(button_data: ButtonData) -> None:
    """Draw the 'Validate key' button."""

    button_surface = button_data['surface']
    if button_data['drawable']:
        button_surface.fill(BUTTON_BG_COLOR)
        write_centered_text(
            'Validate key', button_surface, font_color=BUTTON_FG_COLOR)


def generate_key_selection_buttons_data(cylinder: CYLINDER,
                                        window) -> List[ButtonData]:
    """Compute the button data for every key selection buttons."""

    return [
        generate_key_selection_button_data(cylinder, disk_number, window)
        for disk_number in range(1, len(cylinder) + 1)
    ]


def generate_key_selection_button_data(cylinder: Cylinder,
                                       disk_number: int,
                                       window) -> ButtonData:
    """"""

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
        button_data['clickable'] = False
        button_data['drawable'] = False

    button_data['onclick'] = partial(onclick, button_data)

    return button_data


def draw_key_selection_buttons(buttons_data: List[ButtonData]) -> None:
    """"""

    for button_data in buttons_data:
        draw_key_selection_button(button_data)


def draw_key_selection_button(button_data: ButtonData) -> None:
    """"""

    button_surface = button_data['surface']
    if button_data['drawable']:
        button_surface.fill(BUTTON_BG_COLOR)
        write_centered_text(
            str(button_data['disk_number']),
            button_surface,
            font_color=BUTTON_FG_COLOR)


def draw_key(cylinder: Cylinder, key: Key, window):
    """"""

    for index, key_element in enumerate(key):
        element_dimensions = (window.get_width() / 10 * 9 / len(cylinder),
                              window.get_height() / 10 / 2)
        element_pos = (element_dimensions[0] * index,
                       window.get_height() - element_dimensions[1])
        element_surface = window.subsurface(element_pos, element_dimensions)
        element_surface.fill(WHITE)
        write_centered_text(
            str(key_element), element_surface, font_color=BLACK)


def flatten(l: List[List[Any]]) -> List[Any]:
    """Return a one dimensional list made resulting from the concatenation of
    all the elements of a given two dimensional list."""

    return [x for y in l for x in y]


def clear_surface(surface) -> None:
    """Fill surface with black."""

    surface.fill(BLACK)


if __name__ == "__main__":
    main()
