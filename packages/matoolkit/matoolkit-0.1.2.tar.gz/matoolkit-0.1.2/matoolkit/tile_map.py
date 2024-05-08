import matplotlib.pyplot as plt

from .utils.region_properties import us_labels, us_full_labels, us_rows_to_remove


AVAILABLE_REGIONS = ["us"]


class TileMap:
   """
   A class to create tile maps.
   """

   def __init__(self):
      self.available_regions = AVAILABLE_REGIONS
      self.nrows = None
      self.ncols = None
      self.rows_to_remove = None
      self.default_labels = None
      self.region = None

   def validate_region(self, region):
      """
      Validate the region and return the properties of the region.

      Arguments:
         - region: str, region to validate
      """
      if region not in self.available_regions:
         raise ValueError(f"Region '{region}' not available")
      self.region = region
      return self.us_grid()

   def validate_custom_properties(self, custom_props, expected_length, prop_name):
      """
      Validate the custom properties and return a list with the properties.

      Arguments:
         - custom_props: str, int, list or None, custom properties
         - expected_length: int, expected length of the custom properties
         - prop_name: str, name of the custom properties
      """
      if custom_props:
         if isinstance(custom_props, (str, int)):
               return [custom_props] * expected_length
         elif (
               isinstance(custom_props, list) and len(custom_props) != expected_length
         ):
               raise ValueError(
                  f"{prop_name} must have {expected_length} elements, not {len(custom_props)}"
               )
         return custom_props
      return [None] * expected_length

   def draw_grid(
      self,
      region,
      figsize=(8, 6),
      background_color="white",
      ticks=False,
      tickslabels=False,
      labels=True,
      use_full_labels=False,
      custom_labels=None,
      label_colors=None,
      label_fontsizes=None,
   ):
      """
      Draw a grid with the specified region.
      
      Arguments:
         - region: str, region to draw
         - figsize: tuple, figure size
         - background_color: str, background color of the figure
         - ticks: bool, show ticks
         - tickslabels: bool, show ticks labels
         - labels: bool, show labels
         - use_full_labels: bool, use full labels
         - custom_labels: str, int, list or None, custom labels
         - label_colors: str, int, list or None, custom labels colors
         - label_fontsizes: str, int, list or None, custom labels font sizes
      """
      plt.ioff()

      self.background_color = background_color
      self.ticks = ticks
      self.tickslabels = tickslabels
      self.labels = labels
      self.use_full_labels = use_full_labels

      rows_to_remove, nrows, ncols, default_labels = self.validate_region(region)
      num_cells = nrows * ncols - len(rows_to_remove)
      custom_labels = self.validate_custom_properties(
         custom_labels, num_cells, "Custom labels"
      )
      label_colors = self.validate_custom_properties(
         label_colors, num_cells, "Custom labels colors"
      )
      label_fontsizes = self.validate_custom_properties(
         label_fontsizes, num_cells, "Custom labels font sizes"
      )

      fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
      fig.set_facecolor(background_color)

      i = 0
      for row in range(nrows):
         for col in range(ncols):
            ax = axs[row, col]
            if (row, col) in rows_to_remove:
               ax.remove()
            else:
               ax.set_facecolor(background_color)
               if not ticks:
                  ax.tick_params(axis="both", which="both", length=0)
               if not tickslabels:
                  ax.set_xticklabels([])
                  ax.set_yticklabels([])
               if labels:
                  label = (
                        custom_labels[i] if custom_labels[i] is not None else default_labels[i]
                  )
                  color = (
                        label_colors[i] if label_colors[i] is not None else "black"
                  )
                  fontsize = (
                        label_fontsizes[i] if label_fontsizes[i] is not None else 12
                  )
                  ax.text(
                        0.5,
                        0.5,
                        label,
                        color=color,
                        fontsize=fontsize,
                        ha="center",
                        va="center",
                        transform=ax.transAxes,
                  )
               i += 1

      self.fig = fig
      self.axs = axs
      self.valid_axs = fig.axes
      return fig, fig.axes

   def plot_on_tile(self, df, split_by, col_x, col_y, kind, **kwargs):

      if not hasattr(self, "fig") or not hasattr(self, "axs"):
         raise ValueError("You must call draw_grid() before plot_on_tile()")
      
      # TODO: Implement this method

   def us_grid(self):
      nrows, ncols = 8, 11
      self.nrows = nrows
      self.ncols = ncols

      rows_to_remove = us_rows_to_remove
      self.rows_to_remove = rows_to_remove

      default_labels = us_full_labels if self.use_full_labels else us_labels
      self.default_labels = default_labels

      return rows_to_remove, nrows, ncols, default_labels

