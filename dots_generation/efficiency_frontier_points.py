from markowitz_calc.mu_sigma_helper import *
import numpy as np
from markowitz_calc.efficency_frontier import efficiency_frontier as ef

def provide_points_ef_line(tickers, accuracy:int):
    assert len(tickers) == 2
    #Initialize curve with portfolio-specific variables
    mean, cov = get_portfolio_mean_cov(tickers)
    c = cov.to_numpy()
    m = mean.to_numpy()
    korr = c[0, 1] / (np.sqrt(c[0, 0]) * np.sqrt(c[1, 1]))
    curve = ef(m[0], m[1], np.sqrt(c[0, 0]), np.sqrt(c[1, 1]), korr)
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

def ef_points_given_mu_sigma_kor(m, s, cor, accuracy):
    curve = ef(m[0], m[1], np.sqrt(s[0]), np.sqrt(s[1]), cor)
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

def single_asset_points(tickers):
    mean, cov = get_portfolio_mean_cov(tickers)
    sigmas_asset, mus_asset = [], []
    n_assets = len(tickers)
    for i in range(n_assets):
        w = np.zeros(n_assets)
        w[i] = 1
        mu, sig = calc_mu_sigma(mean, cov, w)
        mus_asset.append(mu)
        sigmas_asset.append(np.sqrt(sig))
    return sigmas_asset, mus_asset