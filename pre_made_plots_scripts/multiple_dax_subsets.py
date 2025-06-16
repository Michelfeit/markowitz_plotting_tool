import colorsys
import random

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from data_fetching.data_management import get_dax_df
from markowitz_calc.mu_sigma_helper import get_dax_index_mean_cov_weights, calc_mu_sigma
from dots_generation.portfolio_scattered_points import provide_points_random_allocation_dax, provide_points_random_allocation


def generate_distinct_colors(n):
    """
    Generate `n` visually distinct, high-saturation colors by spacing hues evenly
    around the HSV/HSB circle. Returns a list of (r, g, b) tuples in [0..1].

    Args:
        n (int): Number of colors to generate.

    Returns:
        List of length‐n, where each item is (r, g, b) with 0 <= r,g,b <= 1.
    """
    step = 1.0 / n
    hues = [(i + 0.5) * step % 1.0 for i in range(n)]  # offset by 0.5 to avoid pure red start

    # Convert each hue→(r, g, b) with saturation=0.9, value=0.95
    return [colorsys.hsv_to_rgb(h, 0.9, 0.95) for h in hues]

df = get_dax_df()
tickers_with_suffix = df['Ticker'] + '.DE'

number_of_subsets = 8
number_of_assets_per_subset = 3
number_of_generated_portfolios = 20000

#Random Dax Portfolios containing all 40 stocks
sigma_dax, mu_dax = provide_points_random_allocation_dax(number_of_generated_portfolios//4)
#Specific DAX allocation
mean_idx, cov_idx, dax_weights = get_dax_index_mean_cov_weights()
μ_idx, σ2_idx = calc_mu_sigma(mean_idx, cov_idx, dax_weights)

# Multiple subset of DAX
samples = [random.sample(range(len(tickers_with_suffix)),
                         number_of_assets_per_subset)
           for _ in range(number_of_subsets)]
subsets_df = pd.DataFrame({'Dax Subset': samples})
ticker_title = []
ms = []
sigs = []
for subset in samples:
    ticker_string = []
    tickers = []
    for i in range(len(subset)):
        ticker_string.append(df['Ticker'][subset[i]])
        tickers.append(tickers_with_suffix[subset[i]])
    ticker_str = ", ".join(ticker_string)
    ticker_title.append(ticker_str)
    sigmas, mus = provide_points_random_allocation(tickers, number_of_generated_portfolios)
    sigs.append(sigmas)
    ms.append([mus])

# Example (n = 5, excluding the “blue” interval 200°−260°):
colors = generate_distinct_colors(number_of_subsets)

subsets_df['Tickers'] = ticker_title
subsets_df['Sigmas'] = sigs
subsets_df['Mus'] = ms


plt.figure(figsize=(8, 6))
plt.xlabel('σ  (portfolio standard deviation)')
plt.ylabel('μ  (expected return)')

plt.title(f"Markowitz μ–σ plot of subsets of DAX")
plt.grid(True, ls='--', alpha=0.3)



for i in range(len(subsets_df)):
    subset = subsets_df.iloc[i]
    s = subset["Sigmas"]
    m = subset["Mus"]
    r, g, b = colors[i]
    string = subset["Tickers"]


    plt.scatter(s, m,
                s=1, alpha=0.5, color=(r,g,b), label=string)

plt.scatter(sigma_dax, mu_dax,
                s=7, alpha=0.5, color="grey", label="DAX random allocation")

plt.scatter(np.sqrt(σ2_idx), μ_idx,
                s=50, alpha=1,marker='X', color="black", label="DAX")
plt.legend()
plt.tight_layout()
plt.show()