import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random

# Fetch stock data
def get_stock_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

# Calculate moving averages
def add_moving_averages(data):
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

def backtest(data, initial_capital):
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

# Replace this list with the 15 stocks you want to analyze
stock_symbols =  ['BK','DAL','INTC','VICI','JCI','PNR','CTRA','CPB','MTCH','HWM','CARR','DD','PARA','KHC','CSCO']
investment_amount = 500
backtest_results = pd.DataFrame(columns=['Symbol', 'Ending_Capital', 'Profits'])

for symbol in stock_symbols:
    data = get_stock_data(symbol, '2020-01-01', '2023-01-01')
    add_moving_averages(data)
    data['Buy_Signal'], data['Sell_Signal'] = simple_moving_average_strategy(data)
    ending_capital, profits = backtest(data, investment_amount)
    
    backtest_results = backtest_results.append({
        'Symbol': symbol,
        'Ending_Capital': ending_capital,
        'Profits': profits
    }, ignore_index=True)

print(backtest_results)
