import numpy as np
from matplotlib import pyplot as plt
from dots_generation.efficiency_frontier_points import ef_points_given_mu_sigma_kor

m = np.array([0.11, 0.07])
s = np.array([0.14, 0.08])


# ------------------------------------------------------------
# 4. plot
# ------------------------------------------------------------

plt.figure(figsize=(8, 6))
# different cases
correlation = -1
sigmas, mus = ef_points_given_mu_sigma_kor(m, s, correlation, 500)
# Plot line connecting the points
plt.plot(sigmas, mus, linestyle='-', color='black', label= "k=-1")

correlation = 1
sigmas, mus = ef_points_given_mu_sigma_kor(m, s, correlation, 500)
# Plot line connecting the points
plt.plot(sigmas, mus, linestyle='-', color='grey', label= "k=1")

correlation = 0
sigmas, mus = ef_points_given_mu_sigma_kor(m, s, correlation, 500)
# Plot line connecting the points
plt.plot(sigmas, mus, linestyle='-', color='red', label= "k=0")

plt.scatter(np.sqrt(s), m,
            s=40, alpha=0.5, color="blue", marker='X', label='Specific Assets')

plt.xlabel('σ  (portfolio standard deviation)')
plt.ylabel('μ  (expected return)')

plt.title(f"Markowitz μ–σ plot of extreme cases of correlation")
plt.grid(True, ls='--', alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()