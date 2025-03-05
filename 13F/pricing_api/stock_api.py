import yfinance as yf


def get_current_price(tick):
    
    stock_symbol = tick  # Replace with desired stock ticker

    stock_data = yf.Ticker(stock_symbol)

    current_price = stock_data.info['regularMarketPrice']

    print(f"Current price of {stock_symbol}: {current_price}") 