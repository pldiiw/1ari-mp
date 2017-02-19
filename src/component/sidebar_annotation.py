"""Functions and procedures used to draw with sidebar annotations."""

from component.write_text import write_left_aligned_text


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
