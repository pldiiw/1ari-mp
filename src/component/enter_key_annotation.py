"""Procedure used to draw our 'Enter key' annotation."""

from component.write_text import write_centered_text


def draw_enter_key_annotation(window) -> None:
    """Draw the 'Enter key' annotation at the right of the key selection
    section (same place as the exit button)."""

    annotation_dimensions = (window.get_width() / 10, window.get_height() / 10)
    annotation_pos = (window.get_width() - annotation_dimensions[0],
                      window.get_height() - annotation_dimensions[1])
    annotation_surface = window.subsurface(annotation_pos,
                                           annotation_dimensions)
    write_centered_text('Enter key', annotation_surface)
