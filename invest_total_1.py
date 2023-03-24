import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Fetch stock data
symbol = 'AAPL'
start_date = '2020-01-01'
end_date = '2023-01-01'

data = yf.download(symbol, start=start_date, end=end_date)

# Calculate moving averages
data['SMA_50'] = data['Close'].rolling(window=50).mean()
data['SMA_200'] = data['Close'].rolling(window=200).mean()

# Simple moving average strategy
def simple_moving_average_strategy(data):
    buy_signals = []
    sell_signals = []
    position = False

    for i in range(len(data)):
        if data['SMA_50'][i] > data['SMA_200'][i] and not position:
            buy_signals.append(data['Close'][i])
            sell_signals.append(np.nan)
            position = True
        elif data['SMA_50'][i] < data['SMA_200'][i] and position:
            sell_signals.append(data['Close'][i])
            buy_signals.append(np.nan)
            position = False
        else:
            buy_signals.append(np.nan)
            sell_signals.append(np.nan)

    return buy_signals, sell_signals

data['Buy_Signal'], data['Sell_Signal'] = simple_moving_average_strategy(data)

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='Close Price', alpha=0.5)
plt.plot(data['SMA_50'], label='50-day SMA', linestyle='--', alpha=0.5)
plt.plot(data['SMA_200'], label='200-day SMA', linestyle='--', alpha=0.5)
plt.scatter(data.index, data['Buy_Signal'], label='Buy', marker='^', color='green')
plt.scatter(data.index, data['Sell_Signal'], label='Sell', marker='v', color='red')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()



def backtest(data, initial_capital=10000):
    capital = initial_capital
    position = 0
    buy_prices = []
    profits = []

    for i in range(len(data)):
        if not np.isnan(data['Buy_Signal'][i]):
            buy_prices.append(data['Buy_Signal'][i])
            position += 1
            capital -= data['Buy_Signal'][i]
        elif not np.isnan(data['Sell_Signal'][i]) and position > 0:
            sell_price = data['Sell_Signal'][i]
            profit = 0

            for buy_price in buy_prices:
                profit += sell_price - buy_price

            profits.append(profit)
            buy_prices = []
            position = 0
            capital += sell_price

    return capital, profits

capital, profits = backtest(data)
print("Ending capital:", capital)
print("Profits:", profits)

