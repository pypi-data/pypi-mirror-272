import pytest
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch
from unittest.mock import MagicMock

from matoolkit.draw_arrow import draw_arrow


@pytest.fixture
def setup_figure():
    fig = Figure()
    fig.transFigure = MagicMock()
    fig.patches = []
    return fig


def test_default_parameters(setup_figure):
    fig = setup_figure
    tail_position = (0.1, 0.1)
    head_position = (0.2, 0.2)
    draw_arrow(tail_position, head_position, fig)
    assert len(fig.patches) == 1
    arrow = fig.patches[0]
    assert arrow.get_color() == "black"
    assert arrow.get_linewidth() == 1.5


def test_inversion_parameter(setup_figure):
    fig = setup_figure
    tail_position = (0.1, 0.1)
    head_position = (0.2, 0.2)
    draw_arrow(tail_position, head_position, fig, invert=True)
    assert "-0.5" in fig.patches[0]._kwargs["connectionstyle"]


def test_different_colors_and_widths(setup_figure):
    fig = setup_figure
    tail_position = (0.1, 0.1)
    head_position = (0.2, 0.2)
    draw_arrow(tail_position, head_position, fig, color="red", lw=2.0)
    arrow = fig.patches[0]
    assert arrow.get_color() == "red"
    assert arrow.get_linewidth() == 2.0


def test_integration_with_matplotlib(setup_figure):
    fig = setup_figure
    tail_position = (0.1, 0.1)
    head_position = (0.2, 0.2)
    draw_arrow(tail_position, head_position, fig)
    assert len(fig.patches) == 1
    assert isinstance(fig.patches[0], FancyArrowPatch)
