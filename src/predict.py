import numpy as np

def predict_next_day(model, last_sequence, scaler):
    last_sequence = last_sequence.reshape((1, last_sequence.shape[0], 1))
    predicted = model.predict(last_sequence)
    predicted_price = scaler.inverse_transform(predicted)
    return predicted_price[0][0]

def predict_series(model, X_start, steps, scaler):
    predictions = []
    current_input = X_start.copy()  # Shape: (1, 60, 1)

    for _ in range(steps):
        # Predict next step
        predicted_scaled = model.predict(current_input, verbose=0)
        # Store the predicted price (unscaled)
        predicted = scaler.inverse_transform(predicted_scaled)[0][0]
        predictions.append(predicted)

        # Update current_input: remove oldest, append predicted_scaled
        predicted_scaled_reshaped = predicted_scaled.reshape((1, 1, 1))
        current_input = np.concatenate((current_input[:, 1:, :], predicted_scaled_reshaped), axis=1)

    return predictions