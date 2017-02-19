"""Functions and procedures used to draw/write text onto the screen."""

from typing import Tuple

import pygame

from gui_parameters import FONT_COLOR, FONT_NAME, FONT_SIZE

# Type aliases
Color = Tuple[int, int, int]


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


def write_left_aligned_text(text: str,
                            parent_surface,
                            font_size: int=FONT_SIZE,
                            font_color: Color=FONT_COLOR) -> None:
    """Draw the given text at the left border of the parent surface."""

    font = pygame.font.Font(pygame.font.match_font(FONT_NAME), font_size)
    text_surface = font.render(text, True, font_color)
    text_pos = text_surface.get_rect(center=(
        0.5 * parent_surface.get_width(), 0.5 * parent_surface.get_height()))
    text_pos.left = 0  # Align text with left border
    parent_surface.blit(text_surface, text_pos)
