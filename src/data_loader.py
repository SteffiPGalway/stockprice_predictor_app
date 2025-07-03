import yfinance as yf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def fetch_stock_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)
    data = df[['Close']].dropna()
    return data

def normalize_data(data):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(data)
    return scaled, scaler