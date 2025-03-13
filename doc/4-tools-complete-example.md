# 4.- Index Tracking tools and a complete example
So far we have used synthetic data for the Index Tracking examples. But as we have defined, the utility function matrix must be a covariance or quadratic distance matrix, which must be calculated from a price history. 

We provide a tool to calculate this data from a covariance history, which we explain in this section. 

## 4.1.- Calculate the covariance matrix
The `compute_covariance_matrix` function computes the covariance matrix of asset returns using an **Exponentially Weighted Moving Average (EWMA)** approach. This method gives greater importance to recent data points while calculating the covariance, making it useful for financial modeling and risk management.

### Function Signature

```python
import pandas as pd

def compute_covariance_matrix(
    assets_index_prices: pd.DataFrame,
    benchmark_column: str,
    date_from: str | pd.Timestamp,
    date_to: str | pd.Timestamp,
    EMWA_halflife: int = 252,
    maximum_missing_data_ratio_allowed: float = 0.25,
    l2_regularization: float = 0.0
):
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `assets_index_prices` | `pd.DataFrame` | N/A | A DataFrame containing time series price data for different assets. Each column represents an asset, and the index represents the date. |
| `benchmark_column` | `str` | N/A | The name of the benchmark asset column used for comparison. |
| `date_from` | `str` or `pd.Timestamp` | N/A | The start date for the covariance calculation period. |
| `date_to` | `str` or `pd.Timestamp` | N/A | The end date for the covariance calculation period. |
| `EMWA_halflife` | `int` | `252` | The half-life parameter for the exponential weighting, measured in trading days. The default is 252, corresponding to one trading year. |
| `maximum_missing_data_ratio_allowed` | `float` | `0.25` | The maximum allowable ratio of missing data points for any asset before exclusion. The default is 0.25 (25%). |
| `l2_regularization` | `float` | `0.0` | The L2 regularization strength, which adds a small value to the diagonal elements of the covariance matrix to improve numerical stability. |

### Returns

The function returns three objects:

- **`cost_matrix`** (`numpy.ndarray`): A square matrix representing the covariance between assets, excluding the benchmark asset.
- **`benchmark_cost_vector`** (`numpy.ndarray`): A vector containing the covariance values of each asset with the benchmark asset.
- **`tickers`** (`list[str]`): A list of asset tickers excluding the benchmark asset.

### Key Features

- **Exponentially Weighted Moving Average (EWMA):**
  - Recent observations are given greater importance compared to older ones.
  - Helps in tracking changes in asset volatility more efficiently.

- **Handles Missing Data:**
  - Assets with too many missing values (above `maximum_missing_data_ratio_allowed`) are excluded from the computation.

- **L2 Regularization:**
  - Helps in conditioning the covariance matrix to avoid numerical instabilities.
  - Useful when dealing with highly correlated assets.

### Example Usage

```python
import pandas as pd
from datetime import datetime
from iq.tools.quadratic_utility import compute_covariance_matrix

# Sample Data
data = {
    "Asset_A": [100, 102, 101, 103, 105],
    "Asset_B": [50, 51, 52, 50, 49],
    "Asset_C": [200, 198, 202, 205, 210]
}
dates = pd.date_range(start="2024-01-01", periods=5, freq='D')
assets_df = pd.DataFrame(data, index=dates)

# Compute covariance matrix
cost_matrix, benchmark_cost_vector, tickers = compute_covariance_matrix(
    assets_index_prices=assets_df,
    benchmark_column="Asset_A",
    date_from="2024-01-01",
    date_to="2024-01-05"
)

print("Cost Matrix:", cost_matrix)
print("Benchmark Cost Vector:", benchmark_cost_vector)
print("Tickers:", tickers)
```


## 4.2.- Calculate the quadratic distance matrix

The `compute_cumulative_returns_distance_matrix` function computes the quadratic distance matrix of asset returns using an **Exponentially Weighted Moving Average (EWMA)** approach. This method assigns greater importance to recent data points when calculating quadratic distances, making it valuable for financial modeling and risk management.

### Function Signature

```python
import pandas as pd

def compute_cumulative_returns_distance_matrix(
    assets_index_prices: pd.DataFrame,
    benchmark_column: str,
    date_from: str | pd.Timestamp,
    date_to: str | pd.Timestamp,
    EMWA_halflife: int = 252,
    maximum_missing_data_ratio_allowed: float = 0.25,
    l2_regularization: float = 0.0
):
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `assets_index_prices` | `pd.DataFrame` | N/A | A DataFrame containing time series price data for different assets. Each column represents an asset, and the index represents the date. |
| `benchmark_column` | `str` | N/A | The name of the benchmark asset column used for comparison. |
| `date_from` | `str` or `pd.Timestamp` | N/A | The start date for the quadratic distance calculation period. |
| `date_to` | `str` or `pd.Timestamp` | N/A | The end date for the quadratic distance calculation period. |
| `EMWA_halflife` | `int` | `252` | The half-life parameter for the exponential weighting, measured in trading days. The default is 252, corresponding to one trading year. |
| `maximum_missing_data_ratio_allowed` | `float` | `0.25` | The maximum allowable ratio of missing data points for any asset before exclusion. The default is 0.25 (25%). |
| `l2_regularization` | `float` | `0.0` | The L2 regularization strength, which adds a small value to the diagonal elements of the quadratic distance matrix to improve numerical stability. |

### Returns

The function returns three objects:

- **`cost_matrix`** (`numpy.ndarray`): A square matrix representing the quadratic distance between assets, excluding the benchmark asset.
- **`benchmark_cost_vector`** (`numpy.ndarray`): A vector containing the quadratic distance values of each asset with the benchmark asset.
- **`tickers`** (`list[str]`): A list of asset tickers excluding the benchmark asset.

### Key Features

- **Exponentially Weighted Moving Average (EWMA):**
  - Recent observations are given greater importance compared to older ones.
  - Helps in tracking changes in asset distance relationships more efficiently.

- **Handles Missing Data:**
  - Assets with too many missing values (above `maximum_missing_data_ratio_allowed`) are excluded from the computation.

- **L2 Regularization:**
  - Helps in conditioning the distance matrix to avoid numerical instabilities.
  - Useful when dealing with highly correlated assets.

### Example Usage

```python
import pandas as pd
from datetime import datetime
from iq.tools.quadratic_utility import compute_cumulative_returns_distance_matrix

# Sample Data
data = {
    "Asset_A": [100, 102, 101, 103, 105],
    "Asset_B": [50, 51, 52, 50, 49],
    "Asset_C": [200, 198, 202, 205, 210]
}
dates = pd.date_range(start="2024-01-01", periods=5, freq='D')
assets_df = pd.DataFrame(data, index=dates)

# Compute cumulative returns distance matrix
cost_matrix, benchmark_cost_vector, tickers = compute_cumulative_returns_distance_matrix(
    assets_index_prices=assets_df,
    benchmark_column="Asset_A",
    date_from="2024-01-01",
    date_to="2024-01-05"
)

print("Cost Matrix:", cost_matrix)
print("Benchmark Cost Vector:", benchmark_cost_vector)
print("Tickers:", tickers)
```

## 4.3.- Calculate an Index Tracking from parameters in files