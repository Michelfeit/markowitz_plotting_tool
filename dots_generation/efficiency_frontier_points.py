from markowitz_calc.mu_sigma_helper import *
import numpy as np
from markowitz_calc.efficency_frontier import efficiency_frontier as ef
"""
This module provides utility functions for computing efficient frontiers and individual asset points
used in Markowitz portfolio analysis.

Functions:
----------
1. provide_points_ef_line(tickers, accuracy):
   Computes points along the efficient frontier for a portfolio consisting of exactly two assets.

2. ef_points_given_mu_sigma_kor(m, s, cor, accuracy):
   Variant of the above that works directly with mean returns, standard deviations, and correlation.

3. single_asset_points(tickers):
   Computes the μ (expected return) and σ (standard deviation) for each individual asset in a list.

Notes:
------
- The 'ef' object is assumed to be a helper class that can compute the efficient frontier
  given asset parameters (expected returns, standard deviations, and correlation).
- The 'get_portfolio_mean_cov' function must return the mean return vector and covariance matrix.
- The 'calc_mu_sigma' function calculates the expected return and variance given weights.
"""

def provide_points_ef_line(tickers, accuracy:int):
    """
    Computes the efficient frontier for a two-asset portfolio.

    Parameters:
    -----------
    tickers : list[str]
        List of two ticker symbols representing the assets.
    accuracy : int
        Number of sample points to compute along the efficient frontier.

    Returns:
    --------
    sigmas : list[float]
        Portfolio standard deviations along the frontier.
    mus : list[float]
        Corresponding expected returns along the frontier.
    """
    assert len(tickers) == 2 # This method is only valid for two assets
    # Get expected returns (mean) and covariance matrix
    mean, cov = get_portfolio_mean_cov(tickers)
    c = cov.to_numpy()
    m = mean.to_numpy()
    # Calculate correlation between the two assets
    korr = c[0, 1] / (np.sqrt(c[0, 0]) * np.sqrt(c[1, 1]))
    # Initialize efficient frontier object
    curve = ef(m[0], m[1], np.sqrt(c[0, 0]), np.sqrt(c[1, 1]), korr)
    # Define the return range from min to max of the two asset returns
    a = min(m[0], m[1])
    b = max(m[0], m[1])

    sigmas, mus = [], []
    for i in range(accuracy+1):
        m_p = a + (b - a) * (i / accuracy)  # Linear interpolation of return
        mus.append(m_p)
        s_p = curve.sigma_portfolio(m_p)  # Get corresponding variance
        sigmas.append(np.sqrt(s_p))  # Convert to standard deviation
    return sigmas, mus

def ef_points_given_mu_sigma_kor(m, s, cor, accuracy):
    """
    Computes the efficient frontier for two assets, using direct μ, σ, and correlation inputs.

    Parameters:
    -----------
    m : list[float]
        List of expected returns for the two assets.
    s : list[float]
        List of variances (not standard deviations!) for the two assets.
    cor : float
        Correlation coefficient between the two assets.
    accuracy : int
        Number of points to compute on the frontier.

    Returns:
    --------
    sigmas : list[float]
        Portfolio standard deviations.
    mus : list[float]
        Corresponding expected returns.
    """
    # Create frontier using given μ, σ, correlation
    curve = ef(m[0], m[1], np.sqrt(s[0]), np.sqrt(s[1]), cor)
    # Define return range between the two assets
    a = m[0]
    b = m[1]
    if a > b:
        temp = a
        a = b
        b = temp

    sigmas, mus = [], []
    for i in range(accuracy+1):
        m_p = a + (b - a) * (i / accuracy)
        mus.append(m_p)
        s_p = curve.sigma_portfolio(m_p)
        # sigmas.append(s_p)
        sigmas.append(np.sqrt(s_p))
    return sigmas, mus

def ef_points_given_curve(curve:ef, accuracy):
    """
    Computes the efficient frontier for two assets, using direct μ, σ, and correlation inputs.

    Parameters:
    -----------
    ef: an existing efficient frontier
    accuracy : int
        Number of points to compute on the frontier.

    Returns:
    --------
    sigmas : list[float]
        Portfolio standard deviations.
    mus : list[float]
        Corresponding expected returns.
    """
    # Define return range between the two assets
    a = curve.mu1
    b = curve.mu2
    if a > b:
        temp = a
        a = b
        b = temp

    sigmas, mus = [], []
    for i in range(accuracy+1):
        m_p = a + (b - a) * (i / accuracy)
        mus.append(m_p)
        s_p = curve.sigma_portfolio(m_p)
        # sigmas.append(s_p)
        sigmas.append(np.sqrt(s_p))
    return sigmas, mus

def single_asset_points(tickers):
    """
    Computes the expected return and standard deviation for each asset individually.

    Parameters:
    -----------
    tickers : list[str]
        List of asset ticker symbols.

    Returns:
    --------
    sigmas_asset : list[float]
        Standard deviations (σ) of each asset.
    mus_asset : list[float]
        Expected returns (μ) of each asset.
    """
    # Get expected return and covariance matrix
    mean, cov = get_portfolio_mean_cov(tickers)
    sigmas_asset, mus_asset = [], []
    n_assets = len(tickers)
    for i in range(n_assets):
        # One-hot vector for the i-th asset (100% allocation)
        w = np.zeros(n_assets)
        w[i] = 1
        # Compute expected return and variance for the single-asset portfolio
        mu, sig = calc_mu_sigma(mean, cov, w)
        mus_asset.append(mu)
        sigmas_asset.append(np.sqrt(sig)) # Convert variance to standard deviation
    return sigmas_asset, mus_asset