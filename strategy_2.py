import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Define your criteria
max_price = 75
min_days_gain = 10
num_samples = 100
target_filtered_stocks = 15

# Define date range
end_date = datetime.today()
start_date = end_date - timedelta(days=30)  # Extend the range to account for weekends and holidays

# Download the list of S&P 500 components
sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
sp500_table = pd.read_html(sp500_url)
sp500_symbols = sp500_table[0]['Symbol'].tolist()

# Randomly sample 100 stocks
random_symbols = random.sample(sp500_symbols, num_samples)

# Initialize a DataFrame to store the filtered stocks
filtered_stocks = pd.DataFrame(columns=['Symbol', 'Price', 'Gain_days', 'Price_change_pct', 'Avg_volume'])

for symbol in random_symbols:
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        last_price = data.iloc[-1]['Close']
        gain_days = (data['Close'].pct_change() > 0).sum()
        price_change_pct = (data.iloc[-1]['Close'] / data.iloc[0]['Close'] - 1) * 100
        avg_volume = data['Volume'].mean()

        if last_price <= max_price and gain_days >= min_days_gain:
            filtered_stocks = filtered_stocks.append({
                'Symbol': symbol,
                'Price': last_price,
                'Gain_days': gain_days,
                'Price_change_pct': price_change_pct,
                'Avg_volume': avg_volume
            }, ignore_index=True)

        if len(filtered_stocks) >= target_filtered_stocks:
            break
    except Exception as e:
        print(f"Error downloading {symbol} data: {e}")

# Save the filtered stocks to a CSV file
filtered_stocks.to_csv('filtered_stocks.csv', index=False)
print(f"Total filtered stocks: {len(filtered_stocks)}")
