from string import ascii_uppercase
from typing import Dict, List

import pygame
from pygame.locals import *

# Type aliases
Disk = str
Cylinder = Dict[int, Disk]
Key = List[int]
Letter = str

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

# GUI globals
CYLINDER = None
WINDOW = None
CLOCK = None
CYLINDER_SURFACE_DIMENSIONS = None
DISK_SURFACE_DIMENSIONS = None
CYLINDER_SURFACE = None
FONT = None


def main() -> None:
    """Takes care of calling the setup and set off the drawing loop."""

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
    global DISK_SURFACE_DIMENSIONS
    global CYLINDER_SURFACE
    global FONT

    pygame.init()

    WINDOW = pygame.display.set_mode(WINDOW_DIMENSIONS)
    pygame.display.set_caption(WINDOW_CAPTION)

    CLOCK = pygame.time.Clock()

    CYLINDER = {i: ascii_uppercase for i in range(1, 10)}

    CYLINDER_SURFACE_DIMENSIONS = (WINDOW_DIMENSIONS[0],
                                   WINDOW_DIMENSIONS[1] / 10 * 9)
    DISK_SURFACE_DIMENSIONS = (CYLINDER_SURFACE_DIMENSIONS[0] / len(CYLINDER),
                               CYLINDER_SURFACE_DIMENSIONS[1])
    CYLINDER_SURFACE = WINDOW.subsurface((0, 0), CYLINDER_SURFACE_DIMENSIONS)

    FONT = pygame.font.Font(pygame.font.match_font(FONT_NAME), FONT_SIZE)


def draw() -> bool:
    """Main drawing procedure, it calls all of the others drawing
    subroutines. If the program must terminates, this subroutine will return
    False to exit the drawing loop.
    """

    clear_surface(WINDOW)
    draw_cylinder(CYLINDER, CYLINDER_SURFACE)
    pygame.display.flip()
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
    """Draw a letter at the index provided on the disk surface."""

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


def clear_surface(surface) -> None:
    """Fill surface with black."""

    surface.fill(BLACK)


if __name__ == "__main__":
    main()
