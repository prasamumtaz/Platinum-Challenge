import os 
import pickle
import numpy as np
from keras.models import load_model

# -------------------------- Define Current Directory ------------------------------------
current_directory = os.path.dirname(os.path.abspath(__file__))

# -------------------------------- MLP Prediction ----------------------------------------

# Vectorizer
file = open(current_directory + "\Model\\feature.p" , "rb")
vectorizer = pickle.load(file)
file.close()

# MLP Model
file = open(current_directory + "\Model\Model_MLP.p", "rb")
model_MLP = pickle.load(file)
file.close()

# MLP Prediction Function
def prediction_MLP(text):
    vect_count = vectorizer.transform([text])
    prediction = model_MLP.predict(vect_count)[0]

    return prediction

# -------------------------------- LSTM Prediction ----------------------------------------
list_sentiment = ['negative', 'neutral', 'positive']

model_LSTM = load_model(current_directory + "\Model\Model_LSTM.keras")

def prediction_LSTM(text):
    prediction = model_LSTM.predict([text])
    polarity = np.argmax(prediction[0])
    sentiment = list_sentiment[polarity]

    return sentiment