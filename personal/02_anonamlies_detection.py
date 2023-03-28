import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
import tensorflow as tf
# from tensorflow.keras.layers import Input, Dense
# from tensorflow.keras.models import Model

# Load your data from an Excel sheet (replace this with your own file path)
data = pd.read_excel("C:/Users/james/OneDrive/Documents/Important_Files/Life_2023/00_organization_of_self/05_data/emans_finances.xlsx")

# # One-hot encode the 'category' feature
# encoder = OneHotEncoder(sparse=False)
# categories_encoded = encoder.fit_transform(data["category"].values.reshape(-1, 1))

# # Normalize the 'money_spent' feature
# scaler = MinMaxScaler()
# money_spent_normalized = scaler.fit_transform(data["money_spent"].values.reshape(-1, 1))

# # Combine the preprocessed features
# preprocessed_data = np.hstack([categories_encoded, money_spent_normalized])

# # Build and train the autoencoder
# input_dim = preprocessed_data.shape[1]
# encoding_dim = 32

# input_layer = Input(shape=(input_dim,))
# encoder_layer = Dense(encoding_dim, activation="relu")(input_layer)
# decoder_layer = Dense(input_dim, activation="sigmoid")(encoder_layer)
# autoencoder = Model(inputs=input_layer, outputs=decoder_layer)

# autoencoder.compile(optimizer="adam", loss="mse")
# autoencoder.fit(preprocessed_data, preprocessed_data, epochs=100, batch_size=32, shuffle=True)

# # Detect anomalies
# reconstructions = autoencoder.predict(preprocessed_data)
# mse = np.mean(np.power(preprocessed_data - reconstructions, 2), axis=1)

# # Set a threshold for anomalies (e.g., the 95th percentile of the reconstruction error)
# threshold = np.percentile(mse, 95)

# # Flag anomalies
# anomalies = mse > threshold

# # Print anomalies
# print("Anomalies:", anomalies)
