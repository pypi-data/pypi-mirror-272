import pytest
import pandas as pd
from matoolkit.multiple_linecharts import multiple_linecharts, ensure_valid_inputs

data = {
    "category": ["A", "A", "B", "B"],
    "x_value": [1, 2, 1, 2],
    "y_value": [10, 20, 15, 25],
}
df = pd.DataFrame(data)


@pytest.fixture
def sample_df():
    return pd.DataFrame(data)


def test_invalid_category_column(sample_df):
    with pytest.raises(ValueError):
        multiple_linecharts(sample_df, "nonexistent", "x_value", "y_value", 1, 2)


def test_color_configurations(sample_df):
    fig, _ = multiple_linecharts(
        sample_df, "category", "x_value", "y_value", 1, 2, colors=["red", "blue"]
    )
    assert fig.axes[0].get_lines()[0].get_color() == "red"
    assert fig.axes[1].get_lines()[0].get_color() == "blue"


def test_warning_for_ignored_secondary_color(sample_df):
    with pytest.warns(UserWarning):
        multiple_linecharts(
            sample_df,
            "category",
            "x_value",
            "y_value",
            1,
            2,
            use_same_color=True,
            secondary_color="red",
        )
