from dots_generation.plot_helper import build_plot
import matplotlib.pyplot as plt

from dots_generation.efficiency_frontier_points import single_asset_points, provide_points_ef_line
from dots_generation.portfolio_scattered_points import provide_points_random_allocation

"""Given list of portfolios, lit of colors, generate plot. Portfolios with more than 2 assets will be generated as
scatter plots. accuracy can be customized all singular assets will be marked with an X.
Special "portfolios exist": DAX, DAXsub """

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

#plt.tight_layout()
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
