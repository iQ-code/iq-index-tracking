import os
import glob
import pandas as pd
import numpy as np

import iq.api.iqrestapi
import iq.tools.quadratic_utility
import iq.finance.index_tracking

# Initialize API credentials
iq.api.iqrestapi.initialize_credentials("<your-api-key>")

# ============================================================
# Configuration
# ============================================================
DATA_DIR         = "data/dispersion_trade"
STOCK_PRICES_DIR = os.path.join(DATA_DIR, "index_stock_data", "filtered_files")
NDX_PRICE_FILE   = os.path.join(DATA_DIR, "index_stock_data", "NDX_full_1day.txt")
OPTIONS_DATA_DIR = os.path.join(DATA_DIR, "options_data", "final_files")
NDX_IV_FILE      = os.path.join(DATA_DIR, "options_data", "NDX_filtered.csv")

BENCHMARK_COLUMN = "NDX Index"
date_from        = "2023-01-03"
date_to          = "2025-12-15"
V_0              = 1.5   # Upper bound for the dispersion IV constraint this time defined as IVstock / IVindex <= V_0
K                = 20    # Number of stocks to include in the portfolio       
# ============================================================
# Load stock close prices and NDX index into a single DataFrame
# ============================================================
PRICE_COLS = ["Date", "Open", "High", "Low", "Close", "Volume"]
NDX_COLS   = ["Date", "Open", "High", "Low", "Close"]

all_close_prices = {}

for filepath in glob.glob(os.path.join(STOCK_PRICES_DIR, "*_full_1day_adjsplitdiv.txt")):
    ticker = os.path.basename(filepath).replace("_full_1day_adjsplitdiv.txt", "")
    df = pd.read_csv(filepath, header=None, names=PRICE_COLS, parse_dates=["Date"], index_col="Date")
    all_close_prices[ticker] = df["Close"]

ndx_df = pd.read_csv(NDX_PRICE_FILE, header=None, names=NDX_COLS, parse_dates=["Date"], index_col="Date")
all_close_prices[BENCHMARK_COLUMN] = ndx_df["Close"]

assets_index_prices = pd.DataFrame(all_close_prices)

print("\nAsset Index Prices (first 5 rows):")
print(assets_index_prices.head())

# ============================================================
# Compute the covariance matrix from stock prices
# ============================================================
cov_matrix, cov_vector, tickers = iq.tools.quadratic_utility.compute_covariance_matrix(
    assets_index_prices=assets_index_prices,
    benchmark_column=BENCHMARK_COLUMN,
    date_from=date_from,
    date_to=date_to,
    EMWA_halflife=252,
    maximum_missing_data_ratio_allowed=0.25,
    l2_regularization=0.01
)

print("\nCovariance Matrix shape:", cov_matrix.shape)
print("\nCovariance Vector:")
print(cov_vector)
print("\nTickers:")
print(tickers)

# ============================================================
# Build the IV linear constraint matrix
#
# Shape: (num_dates, num_tickers)
#   row t, col i = mid_IV_stock_i_on_date_t / mid_IV_index_on_date_t
#
# Per instrument and date: take the nearest expiry, calls only,
# pick the ATM strike (closest to spot). Mid IV = (Bid IV + Ask IV) / 2.
#
# Constraint applied to the portfolio weights w on every date t:
#   0  <=  linear_constraints_matrix @ w  <=  V_0
# ============================================================
def get_daily_front_expiry_call_iv(df_opt, date_from, date_to):
    """Return a Series (index=Trade Date) of mid IV for the nearest-expiry call."""
    df = df_opt[
        (df_opt["Trade Date"] >= date_from) &
        (df_opt["Trade Date"] <= date_to) &
        (df_opt["Call/Put"] == "c")
    ].copy()

    # Keep only the nearest expiry for each trade date
    min_expiry = df.groupby("Trade Date")["Expiry Date"].transform("min")
    df = df[df["Expiry Date"] == min_expiry]

    df["mid_iv"] = (df["Bid Implied Volatility"] + df["Ask Implied Volatility"]) / 2
    return df.set_index("Trade Date")["mid_iv"]


daily_ivs = {}

for ticker in tickers:
    filepath = os.path.join(OPTIONS_DATA_DIR, f"{ticker}_filtered.csv")
    if not os.path.exists(filepath):
        daily_ivs[ticker] = pd.Series(dtype=float)
        continue
    df_opt = pd.read_csv(filepath, parse_dates=["Trade Date", "Expiry Date"])
    daily_ivs[ticker] = get_daily_front_expiry_call_iv(df_opt, date_from, date_to)

# DataFrame: index=dates, columns=tickers — daily front-expiry call IV per stock
iv_df = pd.DataFrame(daily_ivs).sort_index()

# NDX index IV: front-expiry call IV from NDX_filtered.csv
df_ndx_opt = pd.read_csv(NDX_IV_FILE, parse_dates=["Trade Date", "Expiry Date"])
iv_index_series = get_daily_front_expiry_call_iv(df_ndx_opt, date_from, date_to)

# Divide each stock's daily IV by the index IV for that day
# Result shape: (num_dates, num_tickers)
linear_constraints_matrix = (iv_df.div(iv_index_series, axis=0)).to_numpy()

num_dates = linear_constraints_matrix.shape[0]
lower_bounds_vector = np.zeros(num_dates)
upper_bounds_vector = np.full(num_dates, V_0)

print(f"\nIV constraint matrix shape: {linear_constraints_matrix.shape}")
print(f"Date range in IV data: {iv_df.index[0].date()} to {iv_df.index[-1].date()}")

# ============================================================
# Solve for the optimal portfolio allocation
# ============================================================
portfolio, status, error_description = iq.finance.index_tracking.solve_index_tracking(
    description="Index Tracking - Dispersion Trade",
    assets_utility_matrix=cov_matrix,
    assets_to_benchmark_utility_vector=cov_vector,
    portfolio_size=K,
    asset_names=tickers,
    minimum_weight=0.01,
    linear_constraints_matrix=linear_constraints_matrix,
    lower_bounds_vector=lower_bounds_vector,
    upper_bounds_vector=upper_bounds_vector,
    maximum_weight=0.55
)

print("\nOptimal Portfolio Weights:")
portfolio = {asset: round(100 * weight, 4) for asset, weight in portfolio.items()}
print(portfolio)

if status == "Ok":
    print("✅ No errors encountered.")
elif error_description:
    print(f"❌ Error: {error_description}")
