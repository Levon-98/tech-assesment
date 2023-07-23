import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Load trades dataset from the database
engine = create_engine('mysql+mysqlconnector://root:password@db/my_database')
Session = sessionmaker(bind=engine)
session = Session()
trades_df = pd.read_sql_table('trades', engine)
session.close()

# Get a list of unique stock symbols from the trades_df DataFrame
ticker_symbols = trades_df['sym'].unique()

# Create an empty DataFrame to store the price data for all stocks
price_data_all = pd.DataFrame()

# Fetch historical daily price data for each stock
for ticker_symbol in ticker_symbols:
    try:
        price_data = yf.download(ticker_symbol, start='2023-01-01', end='2023-12-31')
        price_data = price_data['Close'].reset_index()
        price_data.rename(columns={'Close': ticker_symbol}, inplace=True)
        price_data_all = pd.concat([price_data_all, price_data.set_index('Date')], axis=1)
    except Exception as e:
        print(f"Failed to download data for {ticker_symbol}: {e}")

# Create an empty DataFrame to store the portfolio performances for each client
portfolio_performances = pd.DataFrame()

# Calculate portfolio value for each trade entry
for ticker_symbol in ticker_symbols:
    trades_subset = trades_df[trades_df['sym'] == ticker_symbol].copy()
    k = trades_subset['qty'] * price_data_all[ticker_symbol]
    trades_subset.loc[:, 'portfolio_value'] = trades_subset['qty'] * price_data_all[ticker_symbol]
    portfolio_performances = pd.concat([portfolio_performances, trades_subset], ignore_index=True)

# Calculate total portfolio value for each client
portfolio_performance = portfolio_performances.groupby(['accid', 'sym'])['portfolio_value'].sum().reset_index()

# Pivot the portfolio_performance DataFrame to have clients as rows and stocks as columns
portfolio_pivot = portfolio_performance.pivot(index='accid', columns='sym', values='portfolio_value')

# Plot Portfolio Performances for each client
plt.figure(figsize=(10, 6))
for ticker_symbol in ticker_symbols:
    plt.plot(portfolio_pivot.index, portfolio_pivot[ticker_symbol], label=ticker_symbol)

import matplotlib.pyplot as plt

# Your code to create the 'portfolio_performances' DataFrame

plt.bar(portfolio_performances['accid'], portfolio_performances['portfolio_value'])
plt.xlabel('Client ID')
plt.ylabel('Portfolio Value')
plt.title('Portfolio Performances for Each Client')
# Save the plot as an image using the Agg backend in the same directory as the script
import os
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'portfolio_performance.png')
plt.savefig(output_path, format='png')

# Close the plot
plt.close()

# Print the path to the saved image so you can check where it is saved inside the Docker container
print(f"Image saved at: {output_path}")