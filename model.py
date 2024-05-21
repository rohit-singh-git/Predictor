import yfinance as yf
from sklearn.exceptions import NotFittedError
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
import pandas as pd
import asyncio

lr_model = LinearRegression()
dtr_model = DecisionTreeRegressor()

data = pd.read_csv("Stock_names.csv")
symbols = data["SYMBOL"].tolist()
stock_info_cache = []


async def fetch_stock_info(symbol):
    ticker = yf.Ticker(f"{symbol}.ns")
    info = ticker.info
    return {
        "symbol": symbol,
        "name": info.get("longName", "")
    }


async def cache_stock_info():
    global stock_info_cache
    stock_info_cache = await asyncio.gather(*(fetch_stock_info(symbol) for symbol in symbols))


async def train_model(stock_name):
    data = yf.Ticker(f'{stock_name}.ns')

    hist = data.history("max")
    if hist.empty:
        raise ValueError(f"No data found for ticker: {stock_name}")

    X = hist[["Open", "High", "Low"]]
    y = hist["Close"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, train_size=0.8, random_state=1)

    lr_model.fit(X_train, y_train)
    dtr_model.fit(X_train, y_train)


def predict(open, high, low):
    try:
        lr = lr_model.predict([[open, high, low]])
        dtr = dtr_model.predict([[open, high, low]])

    except NotFittedError:
        raise ValueError("Models are not trained yet. Please train the models before predicting.")

    return lr[0], dtr[0]

# def get_stock_list():
#     for symbol in symbols:
#         ticker = yf.Ticker(f"{symbol}.ns")
#         info = ticker.info
#         stock_info.append({
#             "symbol": symbol,
#             "name": info.get("longName", "")
#         })
#     return stock_info
