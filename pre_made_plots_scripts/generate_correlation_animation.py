import bisect
import math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from markowitz_calc.efficency_frontier import efficiency_frontier as ef
from dots_generation.efficiency_frontier_points import ef_points_given_mu_sigma_kor, ef_points_given_curve
"""
correlation_animation.py

This script creates an animated visualization of the efficient frontier for a two-asset portfolio,
highlighting how the shape of the frontier changes with varying correlation values between assets.

The animation interpolates the correlation coefficient (ρ) between -1 and 1, showing the continuous
transition in the frontier's curvature. It also overlays the static cases of perfect negative (ρ = -1)
and perfect positive (ρ = 1) correlation for comparison.

Key Features:
-------------
- Efficient frontier curves are generated dynamically using the function `ef_points_given_mu_sigma_kor`.
- A red line animates through changing correlation values to illustrate how diversification benefits vary.
- Individual assets are marked as black "X" markers.
- Axis arrows and custom styling improve visual clarity.
- The final animation is exported as a GIF file (`corr_coefficient.gif`).

Inputs:
-------
- `m`: Expected returns of the two assets.
- `s`: Standard deviations (volatility) of the two assets.
- A sequence of correlation values from -1 to 1, animated smoothly over 200 frames.

Output:
-------
- Animated GIF saved as `corr_coefficient.gif`.
"""

m = np.array([0.5, 0.04])
s = np.array([0.14, 0.08])

# Axis appearance settings
rc = {
    "xtick.direction": "inout",
    "ytick.direction": "inout",
    "xtick.major.size": 5,
    "ytick.major.size": 5,
}

with plt.rc_context(rc):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Draw static correlation curves
    for corr_val, color, label in [(-1, "black", "k=-1"), (1, "grey", "k=1")]:
        sigmas, mus = ef_points_given_mu_sigma_kor(m, s, corr_val, 500)
        ax.plot(sigmas, mus, linestyle='-', color=color, label=label)

    # Dynamic animated line
    (eff_line,) = ax.plot([], [], color='red', lw=2, label='efficent portfolios')
    (ineff_line,) = ax.plot([], [], color='lightcoral' , lw=2, linestyle='--', label='inefficent portfolios')

    # Highlight individual assets
    ax.scatter(np.sqrt(s), m, s=50, alpha=0.5, color="black", marker='X', label='Specific Assets')

    # Axis labels and title
    ax.set_xlabel('σ  (portfolio standard deviation)')
    ax.set_ylabel('μ  (expected return)')
    ax.set_title(f"Markowitz μ–σ plot | Correlation: k = 0")
    ax.grid(True, ls='--', alpha=0.3)

    # Set up axis spine arrows
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Arrow heads on axes
    ax.plot((1), (0), ls="", marker=">", ms=10, color="k",
            transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot((0), (1), ls="", marker="^", ms=10, color="k",
            transform=ax.get_xaxis_transform(), clip_on=False)

    ax.legend(bbox_to_anchor=(0.32, 0.98))

    # Correlation values to animate through
    n_frames = 200
    correlations = np.concatenate([
        np.linspace(0, -1, n_frames // 4),
        np.linspace(-1, 0, n_frames // 4),
        np.linspace(0, 1, n_frames // 4),
        np.linspace(1, 0, n_frames // 4)
    ])

    def update(frame):
        corr = correlations[frame]
        curve = ef(m[0], m[1], np.sqrt(s[0]), np.sqrt(s[1]), corr)
        min_risk_mu, min_risk_sigma = curve.min_risk_point()


        sigmas, mus = ef_points_given_curve(curve, 100)
        index =  np.argmin(sigmas)
        eff_mus = mus[index:]
        eff_sigmas = sigmas[index:]

        if(index < len(sigmas)):
            ineff_sigmas = sigmas[:index+1]
            ineff_mus = mus[:index+1]
        else:
            ineff_sigmas = sigmas[:index]
            ineff_mus = mus[:index]
        eff_line.set_data(eff_sigmas, eff_mus)
        #eff_line.set_label('efficent portfolios')
        ineff_line.set_data(ineff_sigmas, ineff_mus)
        min_risk_point.set_offsets([[min_risk_mu, min_risk_sigma]])
        ax.legend(bbox_to_anchor=(0.32, 0.98))
        ax.set_title(f"Markowitz μ–σ plot | Correlation: k = {corr:.2f}")
        return eff_line, ineff_line

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    min_risk_point = ax.scatter([], [], color='black', s=200, marker='_', label='Minimum risk')
    ani = animation.FuncAnimation(
        fig, update, frames=n_frames, blit=True, interval=100
    )

    ani.save("../images/corr_coefficient.gif", writer='pillow', fps=15)