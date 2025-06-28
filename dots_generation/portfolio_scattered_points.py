from markowitz_calc.mu_sigma_helper import *
import numpy as np
"""
portfolio_scattered_points.py

This module provides functions to generate random portfolio allocations and compute
their expected returns and standard deviations. It supports:

1. Generating scattered points for arbitrary portfolios using uniform random allocations.
2. Doing the same specifically for the DAX index.
3. Computing risk-return characteristics for a user-defined allocation.
"""

def provide_points_random_allocation(tickers, N):
    """
    Generate N random portfolio allocations for a given list of tickers.

    Parameters:
    -----------
    tickers : list[str]
        List of asset ticker symbols to include in the portfolio.
    N : int
        Number of random allocations (scattered points) to generate.

    Returns:
    --------
    sigmas : list[float]
        Standard deviations (σ) of the randomly allocated portfolios.
    mus : list[float]
        Expected returns (μ) of the randomly allocated portfolios.
    """
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
    """
    Generate n random portfolio allocations using DAX index constituents.

    Parameters:
    -----------
    n : int
        Number of random allocations to generate.

    Returns:
    --------
    sigmas : list[float]
        Standard deviations (σ) of the portfolios.
    mus : list[float]
        Expected returns (μ) of the portfolios.
    """
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

def provide_point_for_specific_weights(tickers, weights):
    """
    Compute μ and σ for a portfolio with user-defined weights.

    Parameters:
    -----------
    tickers : list[str]
        List of asset tickers in the portfolio.
    weights : list[float] or np.ndarray
        Portfolio weights, must sum to 1.

    Returns:
    --------
    sigma : float
        Standard deviation (σ) of the portfolio.
    mu : float
        Expected return (μ) of the portfolio.
    """
    # Get mean and covariance
    mean, cov = get_portfolio_mean_cov(tickers)
    # Compute expected return and variance
    m, s = calc_mu_sigma(mean, cov, weights)
    mu = m
    sigma = np.sqrt(s)
    return sigma, mu