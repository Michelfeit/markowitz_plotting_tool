import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize

def build_plot(plt, tickers, sigmas, mus,
               sigmas_assets=None, mus_assets=None,
               color_dots=None, color_assets=None,
               descriptor=None):
    print(len(sigmas), len(mus))
    assert len(sigmas) == len(mus)
    assert len(sigmas_assets) >= 2

    # handle unassigned parameters
    if color_dots is None:
        color_dots = "blue"
    if color_assets is None or color_assets.strip()  == "":
        color_assets = "black"
    if descriptor is not None and descriptor.strip() == "":
        descriptor = ", ".join([t.removesuffix('.DE') for t in tickers])

    # get the right color
    if isinstance(color_dots, list) and all(isinstance(item, str) for item in color_dots):
        cmap = LinearSegmentedColormap.from_list("p", color_dots)
        # Normalize means for color mapping
        norm = Normalize(vmin=np.min(mus), vmax=np.max(mus))
        # Map means to color
        color_dots = cmap(norm(mus))

    # plot the distribution of different portfolio allocations
    if len(tickers) > 2:
        plt.scatter(sigmas, mus,
                    s=10, alpha=0.5, color=color_dots, label=descriptor)
    if len(tickers) == 2:
        plt.plot(sigmas, mus, linestyle='-', color=color_dots , label=descriptor)
    print(tickers)
    print(mus_assets)
    print(sigmas_assets)
    # plot individual assets
    plt.scatter(sigmas_assets, mus_assets,
            s=40, alpha=1, color=color_assets, marker='X')

    return plt
