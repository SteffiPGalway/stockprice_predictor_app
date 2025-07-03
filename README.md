# 📈 Stockprice Predictor App

A Flask web application that predicts the next day's stock price using an LSTM neural network. Users can enter a stock symbol and date range to see a prediction and a plotted comparison of actual vs. predicted prices.

---

## 🚀 Features

- Fetches historical stock data using `yfinance`
- Normalizes and sequences the data for LSTM input
- Trains or loads a saved model (`.h5`)
- Predicts the next day's closing price
- Visualizes prediction vs. actual price
- Simple web interface using Flask

---

## 🛠️ Local Development Setup

Follow these steps to set up and run the project locally:

### 1. Clone the Repository

```
git clone https://github.com/SteffiPGalway/stockprice_predictor_app.git
cd stockprice_predictor_app
```

### 2. Create and Activate a Virtual Environment

```
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```
### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Run with Gunicorn

```
./run_main.sh
```