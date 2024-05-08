import matplotlib.pyplot as plt
import pandas as pd
from highlight_text import ax_text, fig_text
import warnings

from .utils.valid_highlight_text import count_enclosed_strings
from .utils.text_positions import get_x_position


def multiple_linecharts(
    df,
    category: str,
    x_value: str,
    y_value: str,
    nrows: int,
    ncols: int,
    background_color: str = "white",
    text_color: str = "black",
    alpha: float = 0.3,
    use_same_color: bool = True,
    secondary_color: str = "grey",
    linewidth_main: float = 2,
    linewidth_secondary: float = 2,
    colors: str = None,
    display_group_names: bool = True,
    labels: list = None,
    shift_label_y: float = 0,
    shift_annotation_y: float = 0,
    title: str = None,
    title_position: str = "left",
    credit: str = None,
    credit_position: str = "left",
    figsize: tuple = (12, 8),
    dpi: float = 150,
    annot_last_value: bool = True,
    plot: bool = False,
):
    """
    Create multiple line charts in a single figure

    Arguments:
       - df: DataFrame
       - category: str, column name in df
       - x_value: str, column name in df
       - y_value: str, column name in df
       - nrows: int, number of rows in the figure
       - ncols: int, number of columns in the figure
       - background_color: str, background color of the figure
       - text_color: str, text color of the figure
       - alpha: float, transparency of the secondary lines
       - use_same_color: bool, use the same color for main and secondary lines
       - secondary_color: str, color of the secondary lines if use_same_color is False
       - linewidth_main: float, linewidth of the main lines
       - linewidth_secondary: float, linewidth of the secondary lines
       - colors: list, list of colors for each group
       - shift_label_y: float, y adjustment for the group names
       - title: str, title of the figure
       - title_position: str, position of the title
       - credit: str, credit text
       - credit_position: str, position of the credit text
       - figsize: tuple, figure size
       - dpi: float, figure dpi
       - annot_last_value: bool, annotate the last value of each group
       - plot: bool, plot the figure

    Returns:
       - fig, axs: tuple, figure and axes objects

    """

    # Ensure valid inputs
    inputs_valid: bool = ensure_valid_inputs(
        df=df,
        category=category,
        x_value=x_value,
        y_value=y_value,
        nrows=nrows,
        ncols=ncols,
        colors=colors,
        title_position=title_position,
        credit_position=credit_position,
        use_same_color=use_same_color,
        secondary_color=secondary_color,
        labels=labels,
    )
    if inputs_valid:

        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, dpi=dpi)
        fig.set_facecolor(background_color)

        unique_cat = df[category].unique()

        if not colors:
            colors = [text_color] * len(unique_cat)

        # iterate over the groups and axes
        for i, (group, ax) in enumerate(zip(unique_cat, axs.flat)):

            # set the background color
            ax.set_facecolor(background_color)

            # filter for the group
            filtered_df = df[df[category] == group]
            other_groups = unique_cat[unique_cat != group]

            # plot last data point
            if annot_last_value:
                filtered_df = filtered_df.sort_values(by=x_value)
                last_value = filtered_df.iloc[-1][y_value]
                last_date = filtered_df.iloc[-1][x_value]
                ax.plot(
                    last_date,
                    last_value,
                    marker="o",
                    markersize=5,
                    color=colors[i],
                )

                ax_text(
                    last_date,
                    last_value + shift_annotation_y,
                    f"{round(last_value)}",
                    fontsize=7,
                    color=colors[i],
                    fontweight="bold",
                    ax=ax,
                )

            # plot other groups with lighter colors
            for other_group in other_groups:
                other_y = df[y_value][df[category] == other_group]
                other_x = df[x_value][df[category] == other_group]

                if use_same_color:
                    color = colors[i]
                else:
                    color = secondary_color
                ax.plot(
                    other_x,
                    other_y,
                    color=color,
                    alpha=alpha,
                    linewidth=linewidth_secondary,
                )

            # plot the main group
            x = filtered_df[x_value]
            y = filtered_df[y_value]
            ax.plot(x, y, color=colors[i], linewidth=linewidth_main)

            # custom axes
            ax.set_axis_off()
            ax.set_ylim(df[y_value].min(), df[y_value].max())

            # display group names
            if display_group_names:
                y_pos = df[y_value].mean() + shift_label_y
                x_pos = df[x_value].max()
                if labels is not None:
                    text = labels[i]
                else:
                    text = group
                ax_text(
                    x_pos,
                    y_pos,
                    f"<{text}>",
                    va="top",
                    ha="right",
                    fontsize=10,
                    fontweight="bold",
                    color=colors[i],
                    ax=ax,
                )

        # credit
        if credit:
            n_to_highlight = count_enclosed_strings(credit)
            highlight_textprops = [
                {"fontweight": "bold"} for _ in range(n_to_highlight)
            ]
            x_pos = get_x_position(credit_position)
            fig_text(
                x_pos,
                0.01,
                credit,
                fontsize=7,
                ha=credit_position,
                va="center",
                color=text_color,
                highlight_textprops=highlight_textprops,
                fig=fig,
            )

        # title
        if title:
            n_to_highlight = count_enclosed_strings(title)
            highlight_textprops = [
                {"fontweight": "bold"} for _ in range(n_to_highlight)
            ]
            x_pos = get_x_position(title_position)
            fig_text(
                x_pos,
                0.95,
                title,
                fontsize=16,
                ha=title_position,
                va="center",
                color=text_color,
                highlight_textprops=highlight_textprops,
                fig=fig,
            )

        if plot:
            plt.show()

        return (fig, axs)


def ensure_valid_inputs(
    df,
    category,
    x_value,
    y_value,
    nrows,
    ncols,
    colors,
    secondary_color,
    use_same_color,
    title_position,
    credit_position,
    labels,
):

    for col in [category, x_value, y_value]:
        if col not in df.columns:
            raise ValueError(f"{col} not found in the DataFrame columns")

    if df[y_value].dtype not in ["int64", "float64"]:
        raise ValueError(f"{y_value} must be a numerical column")
    if df[x_value].dtype not in ["datetime64[ns]", "int64", "float64"]:
        raise ValueError(f"{x_value} must be a datetime or numerical column")
    if df[category].dtype not in ["object", "category"]:
        raise ValueError(f"{category} must be a categorical column")

    if title_position not in ["left", "center", "right"]:
        raise ValueError(f'title_position must be one of "left", "center", "right"')
    if credit_position not in ["left", "center", "right"]:
        raise ValueError(f'credit_position must be one of "left", "center", "right"')

    if nrows * ncols != len(df[category].unique()):
        raise ValueError(
            f"nrows ({nrows}) * ncols ({ncols}) must be equal to the number of unique values in the category column ({len(df[category].unique())})"
        )

    if labels is not None:
        if len(labels) != len(df[category].unique()):
            raise ValueError(
                f"labels length ({len(labels)}) must be equal to the number of unique values in the category column ({len(df[category].unique())})"
            )

    if secondary_color != "grey" and use_same_color:
        warnings.warn(
            "secondary_color with use_same_color=True will be ignored.", UserWarning
        )

    if colors is not None:

        if len(colors) != len(df[category].unique()):
            raise ValueError(
                f"colors length ({len(colors)}) must be equal to the number of unique values in the category column ({len(df[category].unique())})"
            )

        if len(colors) != nrows * ncols:
            raise ValueError(
                f"colors length ({len(colors)}) must be equal to nrows*ncols ({nrows*ncols})"
            )

    return True


if __name__ == "__main__":
    pass
