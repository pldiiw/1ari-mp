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

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# GUI Parameters
FPS = 60
WINDOW_DIMENSIONS = (1500, 1000)  # (width, heigth)
WINDOW_CAPTION = 'Jefferson Disk'
FONT_NAME = 'FixedSys'
FONT_SIZE = 32
FONT_COLOR = WHITE
BUTTON_FG_COLOR = BLACK
BUTTON_BG_COLOR = WHITE

# GUI globals
CLICKABLE_COMPONENTS = None
CLOCK = None
CYLINDER = None
CYLINDER_SURFACE = None
CYLINDER_SURFACE_DIMENSIONS = None
DISK_SURFACE_DIMENSIONS = None
FINISH_BUTTON_DATA = None
FINISH_BUTTON_DIMENSIONS = None
FINISH_BUTTON_SURFACE = None
FONT = None
MANIPULATION_SURFACE = None
MANIPULATION_SURFACE_DIMENSIONS = None
ROTATION_BUTTONS_DATA = None
ROTATION_BUTTON_DIMENSIONS = None
SIDEBAR_ANNOTATION_DIMENSIONS = None
SIDEBAR_SURFACE = None
SIDEBAR_SURFACE_DIMENSIONS = None
WINDOW = None


def main() -> None:
    """Takes care of calling the setup and setting off the drawing loop."""

    setup()
    pass_to_next_frame = True
    while pass_to_next_frame:
        pass_to_next_frame = draw()


def setup() -> None:
    """Initialize pygame and the various GUI globals."""

    global CLICKABLE_COMPONENTS
    global CLOCK
    global CYLINDER
    global CYLINDER_SURFACE
    global CYLINDER_SURFACE_DIMENSIONS
    global DISK_SURFACE_DIMENSIONS
    global FINISH_BUTTON_DATA
    global FINISH_BUTTON_DIMENSIONS
    global FINISH_BUTTON_SURFACE
    global FONT
    global MANIPULATION_SURFACE
    global MANIPULATION_SURFACE_DIMENSIONS
    global ROTATION_BUTTONS_DATA
    global ROTATION_BUTTON_DIMENSIONS
    global SIDEBAR_ANNOTATION_DIMENSIONS
    global SIDEBAR_SURFACE
    global SIDEBAR_SURFACE_DIMENSIONS
    global WINDOW

    pygame.init()

    WINDOW = pygame.display.set_mode(WINDOW_DIMENSIONS)
    pygame.display.set_caption(WINDOW_CAPTION)

    CLOCK = pygame.time.Clock()

    CYLINDER = {i: ascii_uppercase for i in range(1, 11)}

    CYLINDER_SURFACE_DIMENSIONS = (WINDOW_DIMENSIONS[0] / 10 * 9,
                                   WINDOW_DIMENSIONS[1] / 10 * 9)
    CYLINDER_SURFACE = WINDOW.subsurface((0, 0), CYLINDER_SURFACE_DIMENSIONS)

    MANIPULATION_SURFACE_DIMENSIONS = (
        CYLINDER_SURFACE_DIMENSIONS[0],
        WINDOW_DIMENSIONS[1] - CYLINDER_SURFACE_DIMENSIONS[1])
    MANIPULATION_SURFACE = WINDOW.subsurface(
        (0, CYLINDER_SURFACE_DIMENSIONS[1]), MANIPULATION_SURFACE_DIMENSIONS)

    SIDEBAR_SURFACE_DIMENSIONS = (
        WINDOW_DIMENSIONS[0] - CYLINDER_SURFACE_DIMENSIONS[0],
        CYLINDER_SURFACE_DIMENSIONS[1])
    SIDEBAR_SURFACE = WINDOW.subsurface((CYLINDER_SURFACE_DIMENSIONS[0], 0),
                                        SIDEBAR_SURFACE_DIMENSIONS)

    FINISH_BUTTON_DIMENSIONS = (
        SIDEBAR_SURFACE_DIMENSIONS[0],
        WINDOW_DIMENSIONS[1] - SIDEBAR_SURFACE_DIMENSIONS[1])
    FINISH_BUTTON_SURFACE = WINDOW.subsurface(
        (MANIPULATION_SURFACE_DIMENSIONS[0], SIDEBAR_SURFACE_DIMENSIONS[1]),
        FINISH_BUTTON_DIMENSIONS)

    DISK_SURFACE_DIMENSIONS = (CYLINDER_SURFACE_DIMENSIONS[0] / len(CYLINDER),
                               CYLINDER_SURFACE_DIMENSIONS[1])
    ROTATION_BUTTON_DIMENSIONS = (DISK_SURFACE_DIMENSIONS[0],
                                  MANIPULATION_SURFACE_DIMENSIONS[1] / 2)
    SIDEBAR_ANNOTATION_DIMENSIONS = (SIDEBAR_SURFACE_DIMENSIONS[0],
                                     SIDEBAR_SURFACE_DIMENSIONS[1] / 26)

    ROTATION_BUTTONS_DATA = generate_rotation_buttons_data(len(CYLINDER))
    FINISH_BUTTON_DATA = generate_finish_button_data()
    CLICKABLE_COMPONENTS = ROTATION_BUTTONS_DATA + [FINISH_BUTTON_DATA]

    FONT = pygame.font.Font(pygame.font.match_font(FONT_NAME), FONT_SIZE)


def draw() -> bool:
    """Main drawing procedure, it calls all of the others drawing
    subroutines. If the program must terminates, this subroutine will return
    False to exit the drawing loop.
    """

    # Redraw UI
    clear_surface(WINDOW)
    draw_cylinder(CYLINDER)
    draw_rotation_buttons(ROTATION_BUTTONS_DATA)
    draw_sidebar_annotation("< CLEAR", 9)
    draw_sidebar_annotation("< CIPHERED", 15)
    draw_finish_button(FINISH_BUTTON_DATA)
    pygame.display.flip()

    # Handle events
    for event in pygame.event.get():
        if event.type is QUIT:
            return False  # Abort program
        elif event.type is MOUSEBUTTONUP:
            for clickable_component in CLICKABLE_COMPONENTS:
                abs_component_rect = pygame.Rect(
                    clickable_component['surface'].get_abs_offset(),
                    clickable_component['surface'].get_size())
                if (clickable_component['clickable'] and
                        abs_component_rect.collidepoint(event.pos)):
                    clickable_component['onclick']()

    # Wait the end of the frame
    CLOCK.tick(FPS)
    return True


def draw_cylinder(cylinder: Cylinder) -> None:
    """Given a cylinder, it will draw every disks the cylinder contains onto
    the surface where the cylinder is ought to be drawn (CYLINDER_SURFACE).
    """

    for disk_number, disk in cylinder.items():
        draw_disk(disk, disk_number)


def draw_disk(disk: Disk, disk_number: int) -> None:
    """Given a disk, its position on the cylinder and a surface to draw on,
    this subroutine will draw this disk at the appropriate location.
    """

    disk_dimensions = DISK_SURFACE_DIMENSIONS
    disk_pos = (disk_dimensions[0] * (disk_number - 1), 0)
    disk_rect = pygame.Rect(disk_pos, disk_dimensions)
    disk_surface = CYLINDER_SURFACE.subsurface(disk_rect)
    for letter_number, letter in enumerate(disk):
        draw_letter(letter, letter_number, disk_surface)


def draw_letter(letter: Letter, letter_number: int, disk_surface) -> None:
    """Draw a letter at the index provided onto the disk surface."""

    letter_dimensions = (disk_surface.get_width(),
                         disk_surface.get_height() / 26)
    letter_pos = (0, letter_dimensions[1] * letter_number)
    letter_rect = pygame.Rect(letter_pos, letter_dimensions)
    letter_surface = disk_surface.subsurface(letter_rect)
    write_letter(letter, letter_surface)


def write_letter(letter: Letter, letter_surface) -> None:
    """Write a letter on the provided surface."""

    text_surface = FONT.render(letter, True, FONT_COLOR)
    text_pos = text_surface.get_rect(center=(
        0.5 * letter_surface.get_width(), 0.5 * letter_surface.get_height()))
    letter_surface.blit(text_surface, text_pos)


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


def generate_rotation_buttons_data(amount_of_disks: int) -> List[ButtonData]:
    """Compute all of the information needed to draw the rotation buttons and
    later interact with them.
    """

    return flatten([[
        generate_rotation_button_data(disk_number, True),
        generate_rotation_button_data(disk_number, False)
    ] for disk_number in range(1, amount_of_disks + 1)])


def generate_rotation_button_data(disk_number: int,
                                  does_rotate_up: bool) -> ButtonData:
    """Generate rotation button data for disk disk_number."""

    button_surface_pos = (
        ROTATION_BUTTON_DIMENSIONS[0] * (disk_number - 1),
        MANIPULATION_SURFACE.get_rect().top +
        (0 if does_rotate_up else ROTATION_BUTTON_DIMENSIONS[1]))
    button_surface = MANIPULATION_SURFACE.subsurface(
        button_surface_pos, ROTATION_BUTTON_DIMENSIONS)
    return {
        'type': 'rotation',
        'does_rotate_up': does_rotate_up,
        'surface': button_surface,
        'onclick': partial(rotate_disk_from_cylinder_in_place, CYLINDER,
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
    else:
        button_surface.fill((0, 0, 0, 0))


def generate_finish_button_data() -> ButtonData:
    """Create a dict for later interacting with the finish button."""

    return {
        'type': 'finish',
        'surface': FINISH_BUTTON_SURFACE,
        'onclick': partial(print, 'FINISH'),  # TODO
        'drawable': True,
        'clickable': True
    }


def draw_finish_button(button_data: ButtonData) -> None:
    """Draw the finish button using its button data."""

    button_surface = button_data['surface']
    if button_data['drawable']:
        button_surface.fill(BUTTON_BG_COLOR)

        text_surface = FONT.render('Finish', True, BUTTON_FG_COLOR)
        text_pos = text_surface.get_rect(
            center=(0.5 * button_surface.get_width(),
                    0.5 * button_surface.get_height()))
        button_surface.blit(text_surface, text_pos)
    else:
        button_surface.fill((0, 0, 0, 0))


def draw_sidebar_annotation(text: str, column: int) -> None:
    """Draw an annotated text onto the sidebar at the given column, relative to
    the ones of the disks."""

    annotation_surface = SIDEBAR_SURFACE.subsurface(
        (0, SIDEBAR_ANNOTATION_DIMENSIONS[1] *
         column), SIDEBAR_ANNOTATION_DIMENSIONS)
    text_surface = FONT.render(text, True, WHITE)
    text_pos = text_surface.get_rect(
        center=(0.5 * annotation_surface.get_width(),
                0.5 * annotation_surface.get_height()))
    text_pos.left = 0  # Align annotation with left border
    annotation_surface.blit(text_surface, text_pos)


def flatten(l: List[List[Any]]) -> List[Any]:
    """Return a one dimensional list made resulting from the concatenation of
    all the elements of a given two dimensional list."""

    return [x for y in l for x in y]


def clear_surface(surface) -> None:
    """Fill surface with black."""

    surface.fill(BLACK)


if __name__ == "__main__":
    main()
