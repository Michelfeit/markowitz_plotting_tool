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
