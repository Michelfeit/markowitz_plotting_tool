from data_fetching.yahoo_finance import get_means_and_cov
from data_fetching.data_management import get_dax_df
import numpy as np

def get_random_allocation_mu_cov_uniform(n: int):
    vec = np.random.rand(n)
    vec /= vec.sum()
    return vec

def get_random_allocation_mu_cov_beta(alpha, beta, n: int):
    vec = np.random.beta(alpha, beta, n)
    vec /= vec.sum()
    return vec

def calc_mu_sigma(mean, cov, weights):
    weight_matrix = np.outer(weights, weights)
    weighted_cov = cov.to_numpy() * weight_matrix
    weighted_mean = mean * weights
    mu = np.sum(weighted_mean)
    sigma_2 = np.sum(weighted_cov)
    return mu, sigma_2

def get_portfolio_mean_cov(tickers:list):
    mean, cov = get_means_and_cov(tickers,
                                  "2021-01-01",
                                  None,
                                  "1d",
                                  True,
                                  False)

    # Reindex the mean Series
    mean = mean.reindex(tickers)

    # Reindex the covariance matrix: both rows and columns
    cov = cov.reindex(index=tickers, columns=tickers)
    return mean, cov

def get_dax_index_mean_cov_weights():
    df = get_dax_df()
    tickers_with_suffix = df['Ticker'] + '.DE'
    mean, cov = get_means_and_cov(tickers_with_suffix.tolist(),
                                  "2021-01-01",
                                  None,
                                  "1d",
                                  True,
                                  False)
    weights = df["Share"].to_numpy()
    mean = mean.reindex(tickers_with_suffix)

    # Reindex the covariance matrix: both rows and columns
    cov = cov.reindex(index=tickers_with_suffix, columns=tickers_with_suffix)
    return mean, cov, weights
