from dots_generation.plot_helper import build_plot
import matplotlib.pyplot as plt

from dots_generation.efficiency_frontier_points import single_asset_points, provide_points_ef_line
from dots_generation.portfolio_scattered_points import provide_points_random_allocation, provide_point_for_specific_weights

"""
single_porfolio_plus_scatter.py

This script visualizes the risk-return space of a portfolio using Modern Portfolio Theory.
It generates a scatterplot of randomly weighted portfolios and displays them alongside 
user-defined allocation. 
You may change:
- the tickers in the portfolio variable to display different portfolios.
- the allocation weights in the weight variable. (The index of the weights list corresponds to the ticker with the same
  index in the portfolio list.
- n (the number of randomly-sampled portfolio allocations). 

- Random portfolios are shown in blue.
- The specific allocation is shown as a black 'X'.
"""

# change the list of portfolios to your liking
portfolio = ["SAP.DE", "BAYN.DE", "ALV.DE", 'RHM.DE']
# change the weight to your liking
weight = [3/10, 4/10, 0, 3/10]
assert len(portfolio) == len(weight)
# n is the amount of random allocations
n = 10000

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

sigmas, mus = provide_points_random_allocation(portfolio, n)
sig_1, mu_1 = provide_point_for_specific_weights(portfolio, weight)

min_s = min(sigmas)
if min_s < min_x: min_x = min_s
max_s = max(sigmas)
if max_s > max_x: max_x = max_s

plt.scatter(sigmas, mus,
            s=10, alpha=1, color="blue", label= "random weights")

plt.scatter(sig_1, mu_1,
            s=50, alpha=1, color="black",marker='X', label= "specific weights")

plt.xlim(left= 0)

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