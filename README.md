# Generating Markowitz μ-σ-Plots with real data from yahoofinance:

Harry Markowitz recognized that investors hold multiple assets (diversifying) in order to decrease risk. In his work, Markowitz formalizes risk and makes it tanglible under certain assumptions. Here is a quick rundown of the theory behind this project.

### Theoretical background

In the following paragraphs we assume that the return of a stock follows a Gaussian Distribution and we calculate the mean return of a portfolio as follows: 
Given a portfolio of $N$ assets and their respective mean returns $\mu \in \mathbb{R}^N$ as well as 
their individual portfolio weights $x \in \mathbb{R}^n$ with $\sum_{n}^{N}x_n = 1$, portfolio mean return is:

$$\mu = \sum_{n}^{N} \mu_n * x_n$$

Mean Returns of individual assets are calculated via time series estimation of past closing prices.
Markowitz associates risk with volatility (expressed via variance $\sigma^2$ /standard deviation \sigma)
In order to calculate the risk assotiated with a portfolio and therefore with the mean return, we cannot simply add up individual variances of assets and have to consider their covariances. The covariance $s_{ij}$ between two individuals assets i and j is stated as:

$$s_{ij} = \frac{1}{T-1}\sum_{t}^{T}(x_{i,t}-\mu_i)(x_{j,t}-\mu_j)$$

and the correlation $k_{ij}$ as covariance normalized with individual standard deviations of asset i and j:

$$k_{ij} = \frac{s_{ij}}{\sigma_i \sigma_j}$$

The covariance between two assets allows us to express the covariance matrix $C$ with entries $c_{ij} = s{ij}$. With this we are now able to calculate the portfolio variance (and therefore the risk assotiated with a given protfolio) via the weighted sum over all covariances, as follows:

$$\sigma^2 = x^TCx$$

Assuming we have historical price data and can therefore calculate mean and covariance of assets withing our porfolio as well as the protfolio werights, the afforementioned formualars provide allow us to get the eman and variance of a given portfolio allocation.

### Introduction of this project


# GIF
![](images/corr_coefficient.gif)
*gif caption*
