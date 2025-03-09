import yfinance as yf

#TODO in this file
# Use chatGPT to package into a class

def get_current_price(ticker):
    stock_data = yf.Ticker(ticker)
    current_price = stock_data.info['regularMarketPrice']
    print(f"Current price of {ticker}: {current_price}")

def stock_info(ticker):

    stock_data = yf.Ticker(ticker)
    print(stock_data.fast_info)
    print(stock_data.actions)
    print(stock_data.dividends)
    print(stock_data.splits)
    print(stock_data.analyst_price_targets)
    print(stock_data.balancesheet)
    print(stock_data.cash_flow)
    print(stock_data.fast_info)
    print(stock_data.funds_data)

stock_info("aapl")