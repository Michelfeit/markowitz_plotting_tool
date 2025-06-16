from markowitz_calc.mu_sigma_helper import *
import numpy as np

def provide_points_random_allocation(tickers, N):
    sigmas, mus = [], []
    n_assets = len(tickers)
    mean, cov = get_portfolio_mean_cov(tickers)
    for _ in range(N):
        w = get_random_allocation_mu_cov_uniform(n_assets)              # random weights
        μ, σ2 = calc_mu_sigma(mean, cov, w)                     # your helper
        mus.append(μ)
        sigmas.append(np.sqrt(σ2))
    return sigmas, mus

def provide_points_random_allocation_dax(n):
    sigmas, mus = [], []
    mean, cov, weights = get_dax_index_mean_cov_weights()
    n_assets = len(mean)
    print(n_assets)
    for _ in range(n):
        w = get_random_allocation_mu_cov_uniform(n_assets)              # random weights
        μ, σ2 = calc_mu_sigma(mean, cov, w)                     # your helper
        mus.append(μ)
        sigmas.append(np.sqrt(σ2))
    return sigmas, mus