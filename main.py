from dots_generation.plot_helper import build_plot
import matplotlib.pyplot as plt

from dots_generation.efficiency_frontier_points import single_asset_points, provide_points_ef_line
from dots_generation.portfolio_scattered_points import provide_points_random_allocation

"""
Generates a Markowitz μ–σ plot for a given list of portfolios.

Each portfolio is a list of ticker symbols representing assets. Portfolios with more than
two assets will be plotted as scatter plots using randomly generated allocations, while
two-asset portfolios will be plotted using a deterministic efficient frontier line. 
Each individual asset is also plotted with an 'X' marker.

Parameters:
-----------
portfolios : list[list[str]]
    Nested list where each sublist contains ticker symbols (e.g., "SAP.DE") representing a portfolio.
labels : list[str] or None
    Labels for each portfolio. If None, no legend is displayed. If a label is an empty string, a label
    with ticker symbols will be used automatically.
colors : list[str]
    Colors for plotting the efficiency frontier or scatter distribution of each portfolio.
colors_assets : list[str]
    Colors used for marking the individual assets in each portfolio.
accuracy : int
    Determines the number of allocation samples for portfolios with more than two assets.
x_label : str
    Label for the x-axis (usually standard deviation σ).
y_label : str
    Label for the y-axis (usually expected return μ).
title_diagram : str
    Title displayed on top of the diagram.
compact_x : bool
    If True, compresses the x-axis range to better fit the data.

Notes:
------
- Single assets are marked with an 'X'.
- Axis spines are customized to represent origin-based axes with arrowheads.
- Uses functions: `provide_points_random_allocation`, `provide_points_ef_line`, 
  `single_asset_points`, and `build_plot` (not shown in snippet).
"""

portfolios = [
    ["SAP.DE", "AIR.DE"],
    ["ADS.DE","AIR.DE", "BMW.DE", 'RHM.DE'],
    ["MUV2.DE", "BAYN.DE", 'ALV.DE', 'SAP.DE']
]
labels = [
    "",
    "",
    ""
]
#labels = None
colors = [
    "orange",
    "blue",
    "red"
]
colors_assets = [
    "orange",
    "darkblue",
    "darkred"
]
accuracy = 30000
x_label = 'σ  (portfolio standard deviation)'
y_label = 'μ  (expected return)'
title_diagram = 'Markowitz μ–σ plot'
compact_x = True

fig, ax = plt.subplots(figsize=(8, 6))
# Axis labels and title
ax.set_xlabel(x_label)
ax.set_ylabel(y_label)
ax.set_title(title_diagram)
ax.grid(True, ls='--', alpha=0.3)

plt.grid(True, ls='--', alpha=0.3)

min_x = 10
max_x = 0
all_tickers = list({ticker for portfolio in portfolios for ticker in portfolio})
sigmas_asset, mus_asset = single_asset_points(all_tickers)

for i in range(len(portfolios)):
    if len(portfolios[i]) > 2:
        sigmas, mus = provide_points_random_allocation(portfolios[i], accuracy)
    else:
        sigmas, mus = provide_points_ef_line(portfolios[i], accuracy=min(100, accuracy))
    sigmas_asset, mus_asset = single_asset_points(portfolios[i])
    min_s = min(sigmas)
    if min_s < min_x: min_x = min_s
    max_s = max(sigmas)
    if max_s > max_x: max_x = max_s

    label = None
    if labels:
        label = labels[i]
    plt = build_plot(plt, portfolios[i], sigmas, mus,
                     sigmas_assets=sigmas_asset,
                     mus_assets=mus_asset,
                     color_dots=colors[i],
                     color_assets=colors_assets[i],
                     descriptor=label)
plt.xlim(left= 0)
if len(portfolios) and labels:
    plt.legend()

# Set up axis spine arrows
ax.plot((0), (1), ls="", marker="^", ms=10, color="k",
            transform=ax.get_xaxis_transform(), clip_on=False)
ax.spines['left'].set_position('zero')
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Arrow heads on axes
ax.plot((1), (0), ls="", marker=">", ms=10, color="k",
        transform=ax.get_yaxis_transform(), clip_on=False)

if compact_x:
    delta = (max_x - min_x) * 0.1
    plt.xlim(min_x - delta, max_x + delta)
    ax.spines['left'].set_position(('data', min_x - delta))
    ax.plot((min_x - delta,), (1,), ls="", marker="^", ms=10, color="k",
            transform=ax.get_xaxis_transform(), clip_on=False)
plt.show()
#plt.tight_layout()
