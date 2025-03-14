import pandas as pd
import yfinance as yf
import talib
import backtrader as bt
import matplotlib.pyplot as plt

# Step 1: Download historical data for a stock (e.g., AAPL)
ticker = "AAPL"
df = yf.download(ticker, start="2023-01-01", end="2023-10-31", auto_adjust=False)


# Flatten the DataFrame's columns in case they are MultiIndex or tuples
def flatten_columns(columns):
    new_cols = []
    for col in columns:
        if isinstance(col, tuple):
            # Join tuple elements with an underscore and convert to lowercase
            new_cols.append('_'.join([str(x) for x in col]).lower())
        else:
            new_cols.append(str(col).lower())
    return new_cols


df.columns = flatten_columns(df.columns)

# Rename columns to remove the trailing suffix, e.g. '_aapl'
df.columns = [col.replace('_aapl', '') for col in df.columns]

# Print the columns to verify what names are available
print("DataFrame columns:", df.columns.tolist())

# Convert expected numeric columns to numeric, if they exist
for col in ['open', 'high', 'low', 'close', 'volume']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    else:
        print(f"Warning: Column '{col}' not found. Available columns: {df.columns.tolist()}")

# Step 2: Compute TA-Lib indicators using a flattened 'close' array
close = df['close'].to_numpy().flatten()
df['macd'], df['signal'], df['hist'] = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
df['rsi'] = talib.RSI(close, timeperiod=14)

# Drop rows with NaN values resulting from indicator calculations
df.dropna(inplace=True)


# Step 3: Create a custom PandasData feed with extra columns (macd, signal, hist, rsi)
class PandasDataExtended(bt.feeds.PandasData):
    lines = ('macd', 'signal', 'hist', 'rsi',)
    params = (
        ('macd', -1),
        ('signal', -1),
        ('hist', -1),
        ('rsi', -1),
    )


# Step 4: Define a simple Backtrader strategy using the TA-Lib indicators
class TALibStrategy(bt.Strategy):
    def __init__(self):
        # Reference the TA-Lib computed indicator columns from the data feed
        self.macd = self.data.macd
        self.signal = self.data.signal
        self.rsi = self.data.rsi
        # Create a crossover indicator: +1 when MACD crosses above Signal, -1 when below.
        self.cross = bt.indicators.CrossOver(self.macd, self.signal)

    def next(self):
        if not self.position:
            if self.cross[0] == 1 and self.rsi[0] < 70:
                self.buy(size=100)
                dt = self.data.datetime.date(0)
                print(f"BUY on {dt}, Price: {self.data.close[0]:.2f}")
        elif self.cross[0] == -1 or self.rsi[0] > 70:
            self.sell(size=100)
            dt = self.data.datetime.date(0)
            print(f"SELL on {dt}, Price: {self.data.close[0]:.2f}")


# Step 5: Set up Cerebro and run the backtest
cerebro = bt.Cerebro()
cerebro.addstrategy(TALibStrategy)

data = PandasDataExtended(dataname=df)
cerebro.adddata(data)

cerebro.broker.setcash(100000.0)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Plot without volume to avoid issues if the volume column is missing or invalid
cerebro.plot(style='candlestick', volume=False)
