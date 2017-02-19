"""Functions and procedures used to draw with sidebar annotations."""

import pygame

from component.write_text import write_left_aligned_text

WHITE = (255, 255, 255)


def draw_sidebar_annotation(text: str, column_number: int, window) -> None:
    """Draw an annotated text onto the sidebar (the unused space at the right
    of where the cylinder is drawn) at the given column (aligned with the
    disks' columns).
    """

    annotation_dimensions = (window.get_width() / 10,
                             (window.get_height() / 10 * 9) / 26)
    annotation_pos = (window.get_width() - annotation_dimensions[0],
                      annotation_dimensions[1] * column_number)
    annotation_surface = window.subsurface(annotation_pos,
                                           annotation_dimensions)
    write_left_aligned_text(text, annotation_surface)

    # Add the little delimitation lines
    startpos = (window.get_width() / 10 * 9 / 100 * 5, annotation_pos[1])
    endpos = (window.get_width() / 10 * 9 / 100 * 95, annotation_pos[1])
    pygame.draw.aaline(window, WHITE, startpos, endpos)

    startpos = (startpos[0], startpos[1] + annotation_dimensions[1])
    endpos = (endpos[0], endpos[1] + annotation_dimensions[1])
    pygame.draw.aaline(window, WHITE, startpos, endpos)
