import numpy as np
import random
import iq.api.iqrestapi;
from iq.finance.index_tracking import solve_index_tracking

iq.api.iqrestapi.initialize_credentials("<your-api-key>")


def generate_assets_covariance_matrix(L, rng_seed, ix_missing_data=[]):
    rng = np.random.default_rng(rng_seed)
    r = rng.normal(size=(L, L))
    assets_covariance_matrix = 0.5 * r.T @ r
    if len(ix_missing_data) > 0:
        for ix in ix_missing_data:
            assets_covariance_matrix[ix, :] = 0
            assets_covariance_matrix[:, ix] = 0
            assets_covariance_matrix[ix, ix] = -1
    return assets_covariance_matrix


def generate_index_assets_covariance_vector(L, rng_seed, ix_missing_data=[]):
    rng = np.random.default_rng(rng_seed)
    index_assets_covariance_vector = -0.5 * (1-2*rng.random(size=(L,), dtype=np.double))
    if len(ix_missing_data) > 0:
        for ix in ix_missing_data:
            index_assets_covariance_vector[ix] = 0
    return index_assets_covariance_vector


def generate_names(L):
    return np.array([f"{chr(97 + i)}" for i in range(L)])


def generate_previous_portfolio(L, portfolio_size, rng_seed):
    rng = np.random.default_rng(rng_seed)
    np_previous_portfolio = np.zeros(L)
    np_previous_portfolio[rng.choice(L, portfolio_size, replace=False)] = rng.random(portfolio_size)
    np_previous_portfolio /= np.sum(np_previous_portfolio)
    # Write as dictionary.
    previous_portfolio = {}
    for i in range(L):
        ticker = f"{chr(97 + i)}"
        previous_portfolio[ticker] = np_previous_portfolio[i]
    return previous_portfolio


def generate_inequalities(
    L, n_inequalities,
    lower_bound, upper_bound,
    output,
    rng_seed
):
    rng = np.random.default_rng(rng_seed)

    # Inequality constraints.
    linear_constraints_matrix = rng.random(size=(n_inequalities, L,), dtype=np.double)
    lower_bounds_vector = np.full(n_inequalities, lower_bound, dtype=np.double)
    upper_bounds_vector = np.full(n_inequalities, upper_bound, dtype=np.double)

    if output == "linear_constraints_matrix":
        return linear_constraints_matrix
    elif output == "lower_bounds_vector":
        return lower_bounds_vector
    elif output == "upper_bounds_vector":
        return upper_bounds_vector
    else:
        raise Exception(f"Invalid 'output' argument, must be 'linear_constraints_matrix', 'lower_bounds_vector' or 'upper_bounds_vector'. Currently, it is {output}")

portfolio, info = iq.finance.index_tracking.solve_index_tracking(
                description="IndexTracking: n_assets=10, portfolio_size=7, 3 inequalities",
                assets_covariance_matrix=generate_assets_covariance_matrix(10, 1),
                index_assets_covariance_vector=generate_index_assets_covariance_vector(10, 1),
                portfolio_size=7,
                asset_names=generate_names(10),
                minimum_weight=0.02,
                maximum_weight=0.55,
                linear_constraints_matrix=generate_inequalities(10, 2, 0.05, 0.95, "linear_constraints_matrix", 1),
                lower_bounds_vector=generate_inequalities(10, 2, 0.05, 0.95, "lower_bounds_vector", 1),
                upper_bounds_vector=generate_inequalities(10, 2, 0.05, 0.95, "upper_bounds_vector", 1),
                previous_portfolio=None,
                max_companies_rotation=None,
                max_sales_rotation=None
            )

# Print results
print("Optimal Portfolio Weights:")
print(portfolio)

print("\nSolver Info Code:", info)
if info == 0:
    print("✅ No errors encountered.")
elif info == 1:
    print("❌ Invalid input arguments.")
elif info == 2:
    print("❌ Problem is infeasible.")
elif info == 3:
    print("❌ Computation failed.")

