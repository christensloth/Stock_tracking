import yfinance as yf
import os
import pandas as pd
import sys

def cleanup_directory():
    print("Cleaning up old files")
    current_directory = os.getcwd()
    for filename in os.listdir(current_directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(current_directory, filename)
            os.remove(file_path)
            print(f'Deleted: {file_path}')

def get_tickers():
    with open('stocks_to_track.txt', 'r') as file:
        data = file.readlines()
        
    stock_names_single_string = ' '.join(name.strip() for name in data)
    stock_names_split = stock_names_single_string.split(' ')
    print("You are tracking these stocks:", stock_names_single_string)

    tickers = yf.Tickers(stock_names_single_string)
    return (stock_names_split, tickers)

[split_names, tickers] = get_tickers()

def get_history(name):

# get historical data for the last year => 1y
# Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max"

    history = tickers.tickers[name].history(period="1y",actions=True,auto_adjust=False)
    if history.index.tz is not None:
        history.index = history.index.tz_localize(None)
    history = history[['Open', 'High', 'Low', 'Close', 'Volume']]
    history.insert(0, 'Ticker', name)
    return history
# get actual price for today  => 1d
    history = tickers.tickers[name].history(period="1d",actions=True,auto_adjust=False)
    if history.index.tz is not None:
        history.index = history.index.tz_localize(None)
    history = history[['Open', 'High', 'Low', 'Close', 'Volume']]
    history.insert(0, 'Ticker', name)
    return history

# create ticker for MDLZ Stock
#ticker = yf.Ticker('MDLZ')
# get data of the most recent date
#todays_data = ticker.history(period='1mo',auto_adjust=False)

#print(todays_data)


def fetch_stocks_to_csv():
    all_data = [] 
    for stock_name in split_names:
        all_data.append(get_history(stock_name)) 
    final_data = pd.concat(all_data)
    final_data.to_csv('stocks.csv', index=True)
	
def main():
    cleanup_directory()
    fetch_stocks_to_csv()

if __name__ == "__main__":
    main()