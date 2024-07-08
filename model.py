import pandas as pd
import requests
from io import StringIO
import yfinance as yf
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

lr_model = LinearRegression()
dtr_model = DecisionTreeRegressor()


def get_stock_names_from_github():
    github_raw_url = 'https://raw.githubusercontent.com/rohit-singh-git/Predictor/main/Stock_names.csv'
    response = requests.get(github_raw_url)
    if response.status_code == 200:
        data = pd.read_csv(StringIO(response.text))
        data = data.to_dict(orient="records")
        return data
    else:
        raise ValueError(f"Failed to fetch data from GitHub: {response.status_code}")


# data = pd.read_csv("Stock_names.csv")
# stock_list = data.to_dict(orient="records")
stock_list = get_stock_names_from_github()


def train_model(stock_name):
    data = yf.Ticker(f'{stock_name}.ns')

    hist = data.history("max")
    if hist.empty:
        raise ValueError(f"No data found for ticker: {stock_name}")

    X = hist[["Open", "High", "Low"]]
    y = hist["Close"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

    lr_model.fit(X_train, y_train)
    dtr_model.fit(X_train, y_train)


def predict(open, high, low):
    try:
        lr = lr_model.predict([[open, high, low]])
        dtr = dtr_model.predict([[open, high, low]])

    except NotFittedError:
        raise ValueError("Models are not trained yet. Please train the models before predicting.")

    return lr[0], dtr[0]
