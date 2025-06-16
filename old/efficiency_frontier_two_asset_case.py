import math
import numpy as np
import matplotlib.pyplot as plt
from values import mean, sigma, cov



def calc_portfolio_params_given_2_stocks(i:int, j:int, split_i):
    split = np.array([split_i, 1-split_i])

    cov_ij = np.matrix([
        [cov.item(i,i), cov.item(i,j)],
        [cov.item(j,i), cov.item(j,j)]
    ])

    mean_p = np.matmul(split, np.array([mean[i], mean[j]]))
    variance_p = np.matmul(cov_ij, split)
    variance_p = np.matmul(split, np.ravel(variance_p))
    return mean_p, math.sqrt(variance_p)

limit = 10
for i in range(limit+1):
    split_i = i * 1/limit
    mean_p, sigma_p = calc_portfolio_params_given_2_stocks(0, 5, split_i)
    plt.plot(sigma_p, mean_p, '.', color='b')

ax = plt.gca()
ax.set_xlim([0, .2])
ax.set_ylim([0, .021])
plt.show()


