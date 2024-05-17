from time import sleep

import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

lr_model = LinearRegression()
dtr_model = DecisionTreeRegressor()


# stock_name = 'reliance.ns'


def train_model(stock_name):
    rel = yf.Ticker(f'{stock_name}.ns')

    hist = rel.history("max")

    X = hist[["Open", "High", "Low"]]
    y = hist["Close"]
    sleep(1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, train_size=0.8, random_state=1)

    lr_model.fit(X_train, y_train)
    dtr_model.fit(X_train, y_train)


def predict(open, high, low):
    lr = lr_model.predict([[open, high, low]])
    dtr = dtr_model.predict([[open, high, low]])
    # predicion_result = float(lr[0] + dtr[0]) / 2
    # predicion_result = "{:.3f}".format(predicion_result)
    return lr[0], dtr[0]
