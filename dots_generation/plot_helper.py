import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize

def build_plot(plt, tickers, sigmas, mus,
               sigmas_assets=None, mus_assets=None,
               color_dots=None, color_assets=None,
               descriptor=None):
    """
    Adds a portfolio plot to the existing matplotlib `plt` object.

    Depending on the number of assets in the portfolio:
    - For portfolios with more than 2 assets: plots a scatter of randomly generated allocations.
    - For 2-asset portfolios: plots a line representing the efficient frontier.
    - In all cases, plots individual assets with 'X' markers.

    Parameters:
    -----------
    plt : matplotlib.pyplot
        The current matplotlib plot object to which elements are added.
    tickers : list[str]
        List of asset ticker symbols used in the portfolio.
    sigmas : list[float]
        Portfolio standard deviations (x-axis values).
    mus : list[float]
        Portfolio expected returns (y-axis values).
    sigmas_assets : list[float], optional
        Standard deviations of individual assets.
    mus_assets : list[float], optional
        Expected returns of individual assets.
    color_dots : str or list[str], optional
        Color or color gradient for portfolio allocations.
    color_assets : str, optional
        Color used to mark individual assets.
    descriptor : str, optional
        Label to display in legend. If empty, the list of tickers is used.

    Returns:
    --------
    plt : matplotlib.pyplot
        The updated matplotlib plot object with added portfolio and assets.
    """
    # Ensure portfolio points are valid
    print(len(sigmas), len(mus))
    assert len(sigmas) == len(mus)
    assert len(sigmas_assets) >= 2

    # Handle unassigned parameters
    if color_dots is None:
        color_dots = "blue"
    if color_assets is None or color_assets.strip()  == "":
        color_assets = "black"
    # Generate label if descriptor is empty
    if descriptor is not None and descriptor.strip() == "":
        descriptor = ", ".join([t.removesuffix('.DE') for t in tickers])

    # If a list of colors is provided, map them to μ values using a colormap
    if isinstance(color_dots, list) and all(isinstance(item, str) for item in color_dots):
        cmap = LinearSegmentedColormap.from_list("p", color_dots)
        # Normalize means for color mapping
        norm = Normalize(vmin=np.min(mus), vmax=np.max(mus))
        # Map means to color
        color_dots = cmap(norm(mus))

    # Plot allocation distribution or efficient frontier line
    if len(tickers) > 2:
        # More than 2 assets → use scatter plot for random allocations
        plt.scatter(sigmas, mus,
                    s=10, alpha=0.5, color=color_dots, label=descriptor)
    if len(tickers) == 2:
        # Exactly 2 assets → use line plot for efficient frontier
        plt.plot(sigmas, mus, linestyle='-', color=color_dots , label=descriptor)
    # Mark individual assets with 'X'
    plt.scatter(sigmas_assets, mus_assets,
            s=40, alpha=1, color=color_assets, marker='X')

    return plt
