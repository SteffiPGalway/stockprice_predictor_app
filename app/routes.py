from flask import Blueprint, render_template, request, url_for, current_app
from src.data_loader import fetch_stock_data, normalize_data
from src.predict import predict_next_day
from src.data_loader import fetch_stock_data, normalize_data
from src.model import create_sequences, train_model, load_saved_model, save_model
from src.visualise import plot_predictions
from datetime import datetime
from time import time
import os

bp = Blueprint('main', __name__)

MODEL_PATH = "models/model.h5"

@bp.route("/", methods=["GET", "POST"])
def index():
    current_app.logger.info("Received request to index route!")
    predicted_price = None
    plot_url = None

    # Set default values for GET requests
    symbol = "AAPL"
    start_date = "2020-01-01"
    end_date = "2025-01-01"

    if request.method == "POST":
        symbol = request.form.get("symbol", "AAPL")
        start_date = request.form.get("start_date", "2018-01-01")
        end_date = request.form.get("end_date", "2023-01-01")
        current_app.logger.debug(f"User input: {symbol}")

        # Validate date format
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            if start_dt >= end_dt:
                raise ValueError("Start date must be before end date.")
        except ValueError as ve:
            current_app.logger.error(f"Invalid date range: {ve}")
            return render_template("index.html", predicted_price=None, plot_url=None, error=str(ve))

        # Step 1: Fetch and prepare data
        data = fetch_stock_data(symbol, start_date, end_date)
        current_app.logger.debug(f"Fetched data for {symbol} from {start_date} to {end_date}")
        scaled_data, scaler = normalize_data(data)
        current_app.logger.debug("Data normalized")

        # Create sequences
        X, y = create_sequences(scaled_data)
        current_app.logger.debug(f"Created sequences: X shape {X.shape}, y shape {y.shape}")

        # Step 3: Split train/test
        train_size = int(len(X) * 0.8)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]
        current_app.logger.debug(f"Split data into train and test sets: X_train shape {X_train.shape}, X_test shape {X_test.shape}")

        # Step 4: Check if model already exists
        if os.path.exists(MODEL_PATH):
            model = load_saved_model(MODEL_PATH)
            current_app.logger.info(f"Loaded existing model from {MODEL_PATH}")
        else:
            current_app.logger.info("No existing model found, training a new model")
            # Step 5: Build and train model
            model = train_model(X_train, y_train, epochs=10, batch_size=32)
            current_app.logger.info("Model training completed")
            os.makedirs("models", exist_ok=True)          
            # Step 6: Save the model
            save_model(model, MODEL_PATH)
            current_app.logger.info(f"Model saved to {MODEL_PATH}")
        
         # Step 7: Predict next day price 
        last_sequence = scaled_data[-60:]
        predicted_price = round(predict_next_day(model, last_sequence, scaler), 2)
        current_app.logger.debug(f"Predicted next day price for {symbol}: {predicted_price}")

        # Predict on test set
        predicted = model.predict(X_test)
        current_app.logger.debug("Predicted prices for test set")
        predicted_prices = scaler.inverse_transform(predicted)
        current_app.logger.debug("Inverse transformed predicted prices")
        actual_prices = scaler.inverse_transform(y_test.reshape(-1, 1))
        current_app.logger.debug("Inverse transformed actual prices")

        # Visualize results
        plot_predictions(actual_prices, predicted_prices, save_path='app/static/plot.png')
        current_app.logger.info("Plot saved to app/static/plot.png")

        plot_url = url_for('static', filename='plot.png') + f'?v={int(time())}'  # cache-busting
        current_app.logger.debug(f"Plot URL: {plot_url}")

    return render_template("index.html",  predicted_price=predicted_price, 
                           plot_url=plot_url,
                           symbol=symbol,
                           start_date=start_date,
                           end_date=end_date)