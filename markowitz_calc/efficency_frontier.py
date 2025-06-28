import math

import numpy as np

class efficiency_frontier:
    def __init__(self, mu1, mu2, sigma1, sigma2, korr):
        self.mu1 = mu1
        self.mu2 = mu2
        self.sigma1 = sigma1
        self.sigma2 = sigma2
        self.korr = korr

    def x1(self, mean_return):
        return (mean_return - self.mu2) / (self.mu1 - self.mu2)

    def sigma_portfolio(self, m_p):
        x1 = self.x1(m_p)
        summ1 = (x1 ** 2) * (self.sigma1 ** 2)
        summ2 = ((1 - x1) ** 2) * (self.sigma2 ** 2)
        summ3 = 2 * self.korr * x1 * (1-x1) * self.sigma1 * self.sigma2
        return summ1 + summ2 + summ3

    def min_risk_point(self):
        """Returns the (σ, μ) point of minimal risk on the curve."""
        s1, s2, rho = self.sigma1, self.sigma2, self.korr
        mu1, mu2 = self.mu1, self.mu2

        numerator = s2 ** 2 - rho * s1 * s2
        denominator = s1 ** 2 + s2 ** 2 - 2 * rho * s1 * s2

        x_star = numerator / denominator

        mu = x_star * mu1 + (1 - x_star) * mu2
        sigma2 = self.sigma_portfolio(mu)
        min_mu = min(self.mu1, self.mu2)
        sigma = np.sqrt(sigma2)
        if (mu < min_mu):
            mu = min_mu
            sigma = min(self.sigma1, self.sigma2)
        return sigma, mu
