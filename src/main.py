import yfinance as yf
import os
import pandas as pd

def cleanup_directory():
    print("Cleaning up old files")
    current_directory = os.getcwd()
    for filename in os.listdir(current_directory):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(current_directory, filename)
            os.remove(file_path)
            print(f'Deleted: {file_path}')

def fetch_stocks():
    with open('stocks_to_track.txt', 'r') as file:
        data = file.readlines()
        
    stock_names_single_string = ' '.join(name.strip() for name in data)
    stock_names_split = stock_names_single_string.split(' ')
    print("You are tracking these stocks:", stock_names_single_string)

    tickers = yf.Tickers(stock_names_single_string)
    with pd.ExcelWriter('stocks.xlsx', engine='xlsxwriter') as writer:
        for stock_name in stock_names_split:
            history = tickers.tickers[stock_name].history(period="1mo")
            if history.index.tz is not None:
                history.index = history.index.tz_localize(None)
            history.to_excel(writer, sheet_name=stock_name, index=True)

def main():
    cleanup_directory()
    fetch_stocks()

if __name__ == "__main__":
    main()