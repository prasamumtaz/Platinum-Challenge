# import API library
import pandas as pd
import sqlite3
import os
from flask import Flask
from flask import jsonify
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

#import Data Cleaining library from DataCleaning.py file
import DataCleaning as dc

#import Machine Learning library 
import Prediction as pred

current_directory = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------- FLASK & SWAGGER DEPLOYMENT -----------------------------------------------------
class CustomFlaskAppWithEncoder(Flask):
    json_provider_class = LazyJSONEncoder

app = CustomFlaskAppWithEncoder(__name__)

swagger_template = dict(
    info = {
        "title": "Dokumentasi API untuk Proses Sentiment Analysis",
        "version": "1.0.0",
        "description": "Selamat datang! Ini adalah Server yang digunakan untuk proses analisis sentiment berdasarkan data masukkan (input) yang digunakan. Terdapat 2 macam model yang digunakan untuk melatih (train) machine learning, setiap model memiliki 2 macam data masukkan yang dapat anda gunakan disesuaikan dengan kebutuhan anda. \n**Text Processing** digunakan untuk data masukkan (input) berupa text \n**Upload & Process File CSV - Tweet Cleaning Data** digunakan untuk data masukkan (input) berupa file CSV. \n\nKetentuan penggunanaan dapat anda lihat pada **Terms of service** di bawah. \n\nAnda dapat membantu saya meningkatkan API ini, baik dengan membuat perubahan pada tampilan antarmuka maupun pada proses codingannya. Dengan begitu, saya dapat meningkatkan fitur - fitur lain pada API ini. \nKritik dan saran silahkan hubungi melalui **Contact the developer** di bawah\n\n\n_Referensi terkait Supervised Machine Learning (Data Classification) yang saya gunakan dapat anda cari [disini](https://github.com/prasamumtaz/23001027_14_PFM_API-Data-Cleaning_Challenge-Gold#readme)_\n\nContoh file yang dapat digunakan:\n- [Data](https://bit.ly/ContohData_Input)\n\nDokumen lain yang digunakan pada proses **Cleaning**: \n- [New Kamus Alay](https://bit.ly/NewKamusAlay)",
        "termsOfService": "https://bit.ly/TermofService_CleaningData",
        "contact": {
            "email": "prasamumtaz@gmail.com"
        }
    },
    externalDocs = {
        "description": "(Klik) untuk Data dan Script terkait",
        "url": "https://github.com/prasamumtaz/Platinum-Challenge"
    },
    host = LazyString(lambda: request.host)
)

swagger_config = {
    "headers" : [],
    "specs" : [
        {
            "endpoint": "docs",
            "route" : "/docs.json",
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template, config = swagger_config)

# ------------------------------------------- ENDPOINT MLP ---------------------------------------------
@swag_from("docs/MLP_text_processing.yml", methods=['POST'])
@app.route('/MLP-text', methods=['POST'])
def text_processing_MLP():
    #request to input text
    text = request.form['text']

    #run Clean(text) fuction from CleanData.py to clean input text
    clean_text = dc.clean_data(text)

    sentiment = pred.prediction_MLP(clean_text)

    json_response = {
        'status_code': 200,
        'description': "Teks cleaning process is successful",
        'data': sentiment
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/MLP_processing_file.yml", methods=['POST'])
@app.route('/MLP-file-processing', methods=['POST'])
def upload_processing_file_MLP():

    #CSV File 
	#Upload single CSV File 
    file = request.files['file']

    #read CSV file
    df_fileInput = pd.read_csv(file, encoding='latin1')
    
    #Filter column Tweet column
    df_tweet= pd.DataFrame(df_fileInput[['Tweet']])

    #apply data cleaning fucntion from DataCleaning
    df_tweet['Tweet'] = df_tweet['Tweet'].apply(dc.clean_data)

    #Drop duplicates
    df_tweet= df_tweet.drop_duplicates()
    #Drop Missing Value
    df_tweet = df_tweet.dropna()

    #Prediction
    df_tweet['label'] = df_tweet.Tweet.apply(pred.model_MLP)

    #DataFRame to json
    response_data = df_tweet.to_json(orient='records')

    return response_data

# ------------------------------------------- ENDPOINT LSTM ---------------------------------------------
@swag_from("docs/LSTM_text_processing.yml", methods=['POST'])
@app.route('/LSTM-text', methods=['POST'])
def text_processing_LSTM():
    #request to input text
    text = request.form['text']

    #run Clean(text) fuction from CleanData.py to clean input text
    clean_text = dc.clean_data(text)

    sentiment = pred.prediction_LSTM(clean_text)
    
    json_response = {
        'status_code': 200,
        'description': "Teks cleaning process is successful",
        'data': sentiment
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/LSTM_processing_file.yml", methods=['POST'])
@app.route('/LSTM-file-processing', methods=['POST'])
def upload_processing_file_LSTM():

    #CSV File 
	#Upload single CSV File 
    file = request.files['file']

    #read CSV file
    df_fileInput = pd.read_csv(file, encoding='latin1')
    
    #Filter column Tweet column
    df_tweet= pd.DataFrame(df_fileInput[['Tweet']])

    #apply data cleaning fucntion from DataCleaning
    df_tweet['Tweet'] = df_tweet['Tweet'].apply(dc.clean_data)

    #Drop duplicates
    df_tweet= df_tweet.drop_duplicates()
    #Drop Missing Value
    df_tweet = df_tweet.dropna()

    #Prediction
    df_tweet['label'] = df_tweet.Tweet.apply(pred.model_LSTM)

    #DataFRame to json
    response_data = df_tweet.to_json(orient='records')

    return response_data

if __name__ == '__main__':
   app.run()