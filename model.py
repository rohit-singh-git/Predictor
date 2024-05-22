import pandas as pd
import yfinance as yf
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

lr_model = LinearRegression()
dtr_model = DecisionTreeRegressor()

data = pd.read_csv("Stock_names.csv")
stock_list = data.to_dict(orient="records")




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

