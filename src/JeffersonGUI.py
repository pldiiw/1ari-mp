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
CYLINDER = None
WINDOW = None
CLOCK = None
CYLINDER_SURFACE_DIMENSIONS = None
CYLINDER_SURFACE = None
DISK_SURFACE_DIMENSIONS = None
MANIPULATION_SURFACE_DIMENSIONS = None
MANIPULATION_SURFACE = None
SIDEBAR_SURFACE_DIMENSIONS = None
SIDEBAR_SURFACE = None
ROTATION_BUTTONS_DATA = None
CLICKABLE_COMPONENTS = None
FONT = None


def main() -> None:
    """Takes care of calling the setup and setting off the drawing loop."""

    setup()
    pass_to_next_frame = True
    while pass_to_next_frame:
        pass_to_next_frame = draw()


def setup() -> None:
    """Initialize pygame and the various GUI globals."""

    global WINDOW
    global CLOCK
    global CYLINDER
    global CYLINDER_SURFACE_DIMENSIONS
    global CYLINDER_SURFACE
    global DISK_SURFACE_DIMENSIONS
    global MANIPULATION_SURFACE_DIMENSIONS
    global MANIPULATION_SURFACE
    global SIDEBAR_SURFACE_DIMENSIONS
    global SIDEBAR_SURFACE
    global ROTATION_BUTTONS_DATA
    global CLICKABLE_COMPONENTS
    global FONT

    pygame.init()

    WINDOW = pygame.display.set_mode(WINDOW_DIMENSIONS)
    pygame.display.set_caption(WINDOW_CAPTION)

    CLOCK = pygame.time.Clock()

    CYLINDER = {i: ascii_uppercase for i in range(1, 11)}

    CYLINDER_SURFACE_DIMENSIONS = (WINDOW_DIMENSIONS[0] / 10 * 9,
                                   WINDOW_DIMENSIONS[1] / 10 * 9)
    CYLINDER_SURFACE = WINDOW.subsurface((0, 0), CYLINDER_SURFACE_DIMENSIONS)

    DISK_SURFACE_DIMENSIONS = (CYLINDER_SURFACE_DIMENSIONS[0] / len(CYLINDER),
                               CYLINDER_SURFACE_DIMENSIONS[1])

    MANIPULATION_SURFACE_DIMENSIONS = (CYLINDER_SURFACE_DIMENSIONS[0],
                                       WINDOW_DIMENSIONS[1] - CYLINDER_SURFACE_DIMENSIONS[1])
    MANIPULATION_SURFACE = WINDOW.subsurface(
        (0, CYLINDER_SURFACE_DIMENSIONS[1]), MANIPULATION_SURFACE_DIMENSIONS)

    SIDEBAR_SURFACE_DIMENSIONS = (WINDOW_DIMENSIONS[0] - CYLINDER_SURFACE_DIMENSIONS[0],
                                  WINDOW_DIMENSIONS[1])
    SIDEBAR_SURFACE = WINDOW.subsurface(
        (CYLINDER_SURFACE_DIMENSIONS[0], 0), SIDEBAR_SURFACE_DIMENSIONS)

    ROTATION_BUTTONS_DATA = generate_rotation_buttons_data(
        len(CYLINDER), MANIPULATION_SURFACE)
    CLICKABLE_COMPONENTS = ROTATION_BUTTONS_DATA

    FONT = pygame.font.Font(pygame.font.match_font(FONT_NAME), FONT_SIZE)


def draw() -> bool:
    """Main drawing procedure, it calls all of the others drawing
    subroutines. If the program must terminates, this subroutine will return
    False to exit the drawing loop.
    """

    # Redraw UI
    clear_surface(WINDOW)
    draw_cylinder(CYLINDER, CYLINDER_SURFACE)
    draw_rotation_buttons(ROTATION_BUTTONS_DATA)
    SIDEBAR_SURFACE.fill((255, 0, 0))
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


def draw_cylinder(cylinder: Cylinder, cylinder_surface) -> None:
    """Given a cylinder and a surface to draw on, it will draw every disks the
    cylinder contains.
    """

    for disk_number, disk in cylinder.items():
        draw_disk(disk, disk_number, cylinder_surface)


def draw_disk(disk: Disk, disk_number: int, cylinder_surface) -> None:
    """Given a disk, its position on the cylinder and a surface to draw on,
    this subroutine will draw this disk at the appropriate location.
    """

    disk_dimensions = DISK_SURFACE_DIMENSIONS
    disk_pos = (disk_dimensions[0] * (disk_number - 1), 0)
    disk_rect = pygame.Rect(disk_pos, disk_dimensions)
    disk_surface = cylinder_surface.subsurface(disk_rect)
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


def generate_rotation_buttons_data(amount_of_disks: int,
                                   surface) -> List[ButtonData]:
    """Compute all of the information needed to draw the rotation buttons and
    later interact with them.
    """

    return flatten([[
        generate_rotation_button_data(disk_number, surface, True),
        generate_rotation_button_data(disk_number, surface, False)
    ] for disk_number in range(1, amount_of_disks + 1)])


def generate_rotation_button_data(disk_number: int,
                                  surface,
                                  does_rotate_up: bool) -> ButtonData:
    """Generate rotation button data for disk disk_number."""

    button_surface_dimensions = (DISK_SURFACE_DIMENSIONS[0],
                                 surface.get_height() / 2)
    button_surface_pos = (
        button_surface_dimensions[0] * (disk_number - 1),
        surface.get_rect().top +
        (0 if does_rotate_up else button_surface_dimensions[1]))
    button_surface = surface.subsurface(button_surface_pos,
                                        button_surface_dimensions)
    return {
        'type': 'rotation',
        'does_rotate_up': does_rotate_up,
        'surface': button_surface,
        'onclick': partial(rotate_disk_from_cylinder_in_place, CYLINDER,
                           disk_number, does_rotate_up),
        'clickable': True,
        'drawable': True,
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

    if button_data['drawable']:
        button_data['surface'].fill(BUTTON_BG_COLOR)

        does_rotate_up = button_data['does_rotate_up']
        left = button_data['surface'].get_rect().left
        right = button_data['surface'].get_rect().right
        top = button_data['surface'].get_rect().top
        bottom = button_data['surface'].get_rect().bottom
        point_list = [[left, bottom if does_rotate_up else top],
                      [right / 2, top if does_rotate_up else bottom],
                      [right, bottom if does_rotate_up else top]]
        pygame.draw.aalines(button_data['surface'], BUTTON_FG_COLOR, False,
                            point_list)
    else:
        button_data['surface'].fill((0, 0, 0, 0))


def flatten(l: List[List[Any]]) -> List[Any]:
    """Return a one dimensional list made resulting from the concatenation of
    all the elements of a given two dimensional list."""

    return [x for y in l for x in y]


def clear_surface(surface) -> None:
    """Fill surface with black."""

    surface.fill(BLACK)


if __name__ == "__main__":
    main()
