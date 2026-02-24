from src.data_loader import fetch_stock_data, save_raw_data
from src.data_cleaner import clean_data
from src.metrics import compute_returns, compute_adv, compute_volatility, compute_spread_proxy

ticker = "RELIANCE.NS"

data = fetch_stock_data(ticker)
save_raw_data(data, ticker)

data = clean_data(data)
data = compute_returns(data)
data = compute_adv(data)
data = compute_volatility(data)
data = compute_spread_proxy(data)
