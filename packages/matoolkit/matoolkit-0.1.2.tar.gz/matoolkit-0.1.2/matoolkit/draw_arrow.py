from matplotlib.patches import FancyArrowPatch
from matplotlib.figure import Figure
from typing import Tuple, Optional

# constants for default styling
DEFAULT_TAIL_WIDTH = 1
DEFAULT_HEAD_WIDTH = 5
DEFAULT_HEAD_LENGTH = 5
DEFAULT_COLOR = "black"
DEFAULT_LINE_WIDTH = 1.5


def draw_arrow(
    tail_position: Tuple[float, float],
    head_position: Tuple[float, float],
    fig: Figure,
    invert: bool = False,
    radius: float = 0.5,
    color: str = DEFAULT_COLOR,
    lw: float = DEFAULT_LINE_WIDTH,
    tail_width: float = DEFAULT_TAIL_WIDTH,
    head_width: float = DEFAULT_HEAD_WIDTH,
    head_length: float = DEFAULT_HEAD_LENGTH,
    **kwargs,
) -> None:
    """
    Draw an arrow on a Matplotlib figure.

    Parameters:
    - tail_position (Tuple[float, float]): The (x, y) starting position of the arrow.
    - head_position (Tuple[float, float]): The (x, y) end position of the arrow.
    - fig (Figure): The matplotlib figure to draw the arrow on.
    - invert (bool): If True, invert the curve of the arrow.
    - radius (float): The curvature radius of the arrow.
    - color (str): Color of the arrow.
    - lw (float): Line width of the arrow.
    - tail_width (float): Width of the tail of the arrow.
    - head_width (float): Width of the head of the arrow.
    - head_length (float): Length of the head of the arrow.
    - **kwargs: Additional keyword arguments to pass to the FancyArrowPatch constructor.

    Returns:
    - None
    """

    inputs_valid: bool = ensure_valid_inputs(
        tail_position=tail_position,
        head_position=head_position,
        fig=fig,
        invert=invert,
        radius=radius,
        color=color,
        lw=lw,
        tail_width=tail_width,
        head_width=head_width,
        head_length=head_length,
        **kwargs,
    )
    if inputs_valid:

        arrow_style = f"Simple, tail_width={tail_width}, head_width={head_width}, head_length={head_length}"
        connection_style = f"arc3,rad={'-' if invert else ''}{radius}"
        arrow_patch = FancyArrowPatch(
            tail_position,
            head_position,
            connectionstyle=connection_style,
            transform=fig.transFigure,
            arrowstyle=arrow_style,
            color=color,
            lw=lw,
            **kwargs,
        )
        fig.patches.append(arrow_patch)


def ensure_valid_inputs(
    tail_position,
    head_position,
    fig,
    invert,
    radius,
    color,
    lw,
    tail_width,
    head_width,
    head_length,
    **kwargs,
) -> bool:
    """
    Ensure valid inputs for the draw_arrow function.

    Parameters:
    - tail_position (Tuple[float, float]): The (x, y) starting position of the arrow.
    - head_position (Tuple[float, float]): The (x, y) end position of the arrow.
    - fig (Figure): The matplotlib figure to draw the arrow on.
    - invert (bool): If True, invert the curve of the arrow.
    - radius (float): The curvature radius of the arrow.
    - color (str): Color of the arrow.
    - lw (float): Line width of the arrow.
    - tail_width (float): Width of the tail of the arrow.
    - head_width (float): Width of the head of the arrow.
    - head_length (float): Length of the head of the arrow.
    - **kwargs: Additional keyword arguments to pass to the FancyArrowPatch constructor.

    Returns:
    - bool: True if all inputs are valid, False otherwise.
    """

    if not isinstance(tail_position, tuple) or len(tail_position) != 2:
        raise ValueError(
            f"tail_position must be a tuple of two floats, not: {tail_position}"
        )
    if not all(isinstance(x, (int, float)) for x in tail_position):
        raise ValueError(
            f"tail_position must be a tuple of two floats, not: {tail_position}"
        )

    if not isinstance(head_position, tuple) or len(head_position) != 2:
        raise ValueError(
            f"head_position must be a tuple of two floats, not: {head_position}"
        )
    if not all(isinstance(x, (int, float)) for x in head_position):
        raise ValueError(
            f"head_position must be a tuple of two floats, not: {head_position}"
        )

    if not isinstance(fig, Figure):
        raise ValueError(f"fig must be a Figure object, not: {fig}")

    if not isinstance(invert, bool):
        raise ValueError(f"invert must be a boolean, not: {invert}")

    if not isinstance(color, str):
        raise ValueError(f"color must be a string, not: {color}")

    return True
