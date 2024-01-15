import os 
import json
import pickle
import numpy as np
import pandas as pd
from keras.models import load_model

# -------------------------- Define Current Directory ------------------------------------
current_directory = os.path.dirname(os.path.abspath(__file__))

# Vectorizer
file = open(current_directory + "\Model\\count_vect.p" , "rb")
vectorizer = pickle.load(file)
file.close()

# MLP Model
file = open(current_directory + "\Model\Model_MLP.p", "rb")
model_MLP = pickle.load(file)
file.close()

list_sentiment = ['negative', 'neutral', 'positive']

model_LSTM = load_model(current_directory + "\Model\Model_LSTM.keras")

def text_prediction(text: str, model: str):
    if model == 'MLP':
        vect_count = vectorizer.transform([text])
        sentiment = model_MLP.predict(vect_count)[0]
        
    elif model == 'LSTM':
        prediction = model_LSTM.predict([text])
        polarity = np.argmax(prediction[0])
        sentiment = list_sentiment[polarity]

    return sentiment
    
def CSV_prediction(df: pd.core.frame.DataFrame, model: str, json_out=True):
    if model == 'MLP':
        Data = df.Tweet.tolist()
        count_v = vectorizer.transform(Data)
        #prediction 
        label = model_MLP.predict(count_v)
        
    elif model == 'LSTM':
        Data = np.array(df.Tweet)
        prediction = model_LSTM.predict(Data, batch_size=32)

        #prediction looping
        label = []
        for i in range(len(prediction)):
            polarity = np.argmax(prediction[i])
            sentiment = list_sentiment[polarity]

            label.append(sentiment)
    
    #json looping
    list_Tweet_Label = []
    for i in range(len(Data)):
        list_Tweet_Label.append({"Tweet" : Data[i], "Label" : label[i]})

    if json_out == True:
        json_akhir = json.dumps(list_Tweet_Label, indent = 1)
    else:
        json_akhir = list_Tweet_Label

    return json_akhir