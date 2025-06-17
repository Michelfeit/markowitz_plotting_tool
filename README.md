# Generating Markowitz μ-σ-Plots with real data from yahoofinance:

Harry Markowitz recognized that investors hold multiple assets (diversifying) in order to decrease risk.<br>
In his work, Markowitz formalizes risk and makes it tanglible under certain assumptions.<br>
In the following paragraphs we assume that the return of a stock follows a Gaussian Distribution and we calculate the mean return of a portfolio as follows: 
Given a portfolio of $N$ assets and their respective mean returns $\mu \in \mathbb{R}^N$ as well as 
their individual portfolio weights $x \in \mathbb{R}^n$ with $\sum_{n}^{N}x_n = 1$, portfolio mean return is: <br>

$$\mu_p = \sum_{n}^{N} \mu_n * x_n$$ <br>

Mean Returns of individual assets are calculated via time series estimation of past closing prices.
Markowitz associates risk with volatility (expressed via variance $\sigma^2$ /standard deviation \sigma)
In order to calculate the risk assotiated with a portfolio and therefore with the mean return, we cannot simply add up individual variances of assets and have to consider their covariances. The covariance $s_{ij}$ between two individuals assets i and j is stated as: <br>

$$s_{ij} = \frac{1}{T-1}\sum_{t}^{T}(x_{i,t}-\mu_i)(x_{j,t}-\mu_j)$$ <br>

and the correlation $k_{ij}$ as covariance normalized with individual standard deviations of asset i and j: <br>

$$k_{ij} = \frac{s_{ij}}{\sigma_i \sigma_j}$$ <br>


# GIF
![](images/corr_coefficient.gif)
*gif caption*
