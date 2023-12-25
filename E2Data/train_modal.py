import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
from fetch_data import fetch_data  # Import the fetch_data function

# ANSI escape codes for text colors
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'  # Reset color

def print_color(message, color):
    print(color + message + Colors.ENDC)

def preprocess_and_train(data):
    print_color("Preprocessing and Training...", Colors.HEADER)

    # Assume 'Value' is the target variable
    X = data.drop(['Value'], axis=1)
    y = data['Value']

    # Identify and convert non-numeric columns to numeric
    non_numeric_columns = X.select_dtypes(exclude=['number']).columns
    X[non_numeric_columns] = X[non_numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Drop columns with NaN values (optional, depending on your data)
    X = X.dropna(axis=1)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize the features (optional but often beneficial)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Build a simple regression model (adjust for classification, etc.)
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
        tf.keras.layers.Dense(1)  # Assuming a regression task, adjust for classification
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')  # Adjust loss for classification

    # Train the model
    model.fit(X_train_scaled, y_train, epochs=10, validation_data=(X_test_scaled, y_test))

    print_color("Training completed successfully!", Colors.OKGREEN)

    return model

if __name__ == "__main__":
    df = fetch_data() #Fetch data from E2
    model = preprocess_and_train(df)
    # Save the trained model
    model.save('my_model.keras')

