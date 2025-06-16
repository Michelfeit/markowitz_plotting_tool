import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dots_generation.efficiency_frontier_points import ef_points_given_mu_sigma_kor

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
    (dynamic_line,) = ax.plot([], [], color='red', lw=2, label='k = animated')

    # Highlight individual assets
    ax.scatter(np.sqrt(s), m, s=50, alpha=0.5, color="black", marker='X', label='Specific Assets')

    # Axis labels and title
    ax.set_xlabel('σ  (portfolio standard deviation)')
    ax.set_ylabel('μ  (expected return)')
    ax.set_title("Markowitz μ–σ plot of extreme cases of correlation")
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
        sigmas, mus = ef_points_given_mu_sigma_kor(m, s, corr, 100)
        dynamic_line.set_data(sigmas, mus)
        dynamic_line.set_label(f"k = {corr:.2f}")
        ax.legend(bbox_to_anchor=(0.32, 0.98))
        return dynamic_line,

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ani = animation.FuncAnimation(
        fig, update, frames=n_frames, blit=True, interval=100
    )

    ani.save("corr_coefficient.gif", writer='pillow', fps=15)