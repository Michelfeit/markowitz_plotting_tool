import matplotlib.pyplot as plt
from markowitz_calc.mu_sigma_helper import *


# ------------------------------------------------------------
# 1. get the DAX inputs (mean vector, cov‑matrix, index weights)
# ------------------------------------------------------------
mean, cov, dax_weights = get_dax_index_mean_cov_weights()   # your helper
n_assets = len(mean)

# ------------------------------------------------------------
# 2. generate many random portfolios
# ------------------------------------------------------------
N = 10000                              # how many blue dots you want
sigmas, mus = [], []
sample = False

for i in range(N):
    w = np.zeros(n_assets)
    if(sample):
        w = get_random_allocation_mu_cov_uniform(n_assets) # random weights
    else:
        if i < N/2:
            w = get_random_allocation_mu_cov_beta(100,1,n_assets)
        else:
            w = get_random_allocation_mu_cov_beta(1,100,n_assets)

    μ, σ2 = calc_mu_sigma(mean, cov, w)                     # your helper
    mus.append(μ)
    sigmas.append(np.sqrt(σ2))                              # std‑dev = √variance

# ------------------------------------------------------------
# 3. single red dot for the index weighting itself
# ------------------------------------------------------------
μ_idx, σ2_idx = calc_mu_sigma(mean, cov, dax_weights)
sigma_idx     = np.sqrt(σ2_idx)

# ------------------------------------------------------------
# 4. plot
# ------------------------------------------------------------
plt.figure(figsize=(8, 6))
plt.scatter(sigmas, mus,
            s=10, alpha=0.5, color='steelblue', label='Random portfolios')
plt.scatter(sigma_idx, μ_idx,
            s=100, color='crimson', marker='X', label='DAX index weights')
plt.xlabel('σ  (portfolio standard deviation)')
plt.ylabel('μ  (expected return)')
plt.title('Markowitz μ–σ plot for the DAX universe')
plt.grid(True, ls='--', alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()