from dots_generation.plot_helper import build_plot
import matplotlib.pyplot as plt

from dots_generation.efficiency_frontier_points import single_asset_points, provide_points_ef_line
from dots_generation.portfolio_scattered_points import provide_points_random_allocation

"""Given list of portfolios, lit of colors, generate plot. Portfolios with more than 2 assets will be generated as
scatter plots. accuracy can be customized all singular assets will be marked with an X.
Special "portfolios exist": DAX, DAXsub """

portfolios = [
    ["SAP.DE","P911.DE", "BAYN.DE", "RHM.DE"],
    ["RHM.DE", "PLTR"],
    ["AMD","NVDA","SNOW", "CRWD", "PLTR"]
]
labels = ["", "", "this is a test"]
colors = ["green", "blue", "red"]
colors_assets = ["", "", "red"]

accuracy = 10000
x_label = 'σ  (portfolio standard deviation)'
y_label = 'μ  (expected return)'
title_diagram = 'Markowitz μ–σ plot'



plt.figure(figsize=(8, 6))
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.title(title_diagram)

plt.grid(True, ls='--', alpha=0.3)

#plt.tight_layout()
all_tickers = list({ticker for portfolio in portfolios for ticker in portfolio})
sigmas_asset, mus_asset = single_asset_points(all_tickers)

for i in range(len(portfolios)):
    if len(portfolios[i]) > 2:
        sigmas, mus = provide_points_random_allocation(portfolios[i], accuracy)
    else:
        sigmas, mus = provide_points_ef_line(portfolios[i], accuracy=min(100, accuracy))
    sigmas_asset, mus_asset = single_asset_points(portfolios[i])
    plt = build_plot(plt, portfolios[i], sigmas, mus,
                     sigmas_assets=sigmas_asset,
                     mus_assets=mus_asset,
                     color_dots=colors[i],
                     color_assets=colors_assets[i],
                     descriptor=labels[i])
plt.xlim(left= 0)
if len(portfolios) < 8:
    plt.legend()
plt.show()
