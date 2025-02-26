# 1.- Index Tracking

## 1.1.- The index tracking problem

The index tracking problem consists on selecting a portfolio of $k$ assets from a benchmark index such that the returns of the portfolio track the returns of the index as close as possible. This closeness of the returns during a specific time window is measured by the tracking error, defined as the standard deviation of the difference between the returns of the index and the portfolio 

$$
\mathrm{TE}^2 = \textrm{Var}\left[r_I(t) - r_p(t)\right],
$$

with $r_I(t),r_p(t)$ the returns of the index and the portfolio, respectively, during the time window. 

We define a tracker portfolio by a vector of weights $\vec{\omega}$, whose elements $\omega_i$ define the allocation weight of asset $i$ inside the portfolio. Using this notation, the TE is written as

$$\textrm{TE}^2 = \sigma_I^2 - 2\, \vec{\omega}\,\vec{g} + \vec{\omega}\,\sigma\,\vec{\omega},$$

with $\sigma_I^2$ the variance of the index' returns, $\vec{g}$ the vector of covariance between the assets' and index returns, and $\sigma$ the covariance matrix of the assets' returns.

In general, a portfolio manager must satisfy some restrictions when building a tracker portfolio and at the same time the manager should try to reduce the transaction costs. In iQ-Finance we provide a series of constraints that apply both restrictions:

1. Constraints that reduce the transaction costs: these constraints aim to reduce the transaction costs when we rebalance a portfolio. They use a previous portfolio - `previous_portfolio` in the API - from which they define two rotation constraints

    * Ticker rotation: the number of assets that leaves the portfolio at one rebalance. It can be set to be below a maximum number, which is defined as `max_companies_rotation` in the API.

    * Turnover rotation: the weight of the assets that is sold from the portfolio at one rebalance. It can be set to be below a maximum number, which is defined as `max_sales_rotation` in the API. Its mathematical definition is 
    
    
    $$
        \frac{1}{2}\sum_i |w_i(t) - w_i(t-1)| \leq max\ sales\ rotation.
    $$

2. Constraints that define the weight allocation: the `maximum_weight` and `minimum_weight` constraints define the maximum and minimum allocation weight of an asset inside the tracker portfolio, respectively. These are given as 0 to 1 numbers. E.g. a 8% weight is given as 0.08.

## 1.2.- Index Tracking API


