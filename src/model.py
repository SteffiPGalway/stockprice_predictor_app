import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import load_model

def create_sequences(data, window_size=60):
    X, y = [], []
    for i in range(window_size, len(data)):
        X.append(data[i-window_size:i])
        y.append(data[i])
    return np.array(X), np.array(y)

def build_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_model(model,X_train, y_train, epochs=10, batch_size=32):
    """
    Builds and trains the LSTM model on the training data.

    Args:
        X_train (np.array): Input features for training.
        y_train (np.array): Target values for training.
        epochs (int): Number of training epochs.
        batch_size (int): Size of training batches.

    Returns:
        model: Trained Keras model.
    """
    # Step 1: Build the model
    model = build_model((X_train.shape[1], 1))

    # Step 2: Train the model
    print("Starting model training...")
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)
    print("Model training completed.")

    return model

def load_saved_model(filename='model.h5'):
    return load_model(filename)     

def save_model(model, filename='model.h5'):
    model.save(filename)