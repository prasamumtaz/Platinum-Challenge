# import API library
import os
import pandas as pd
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
        "description": """
                        \nSelamat datang! Ini adalah Server yang digunakan untuk proses analisis sentiment berdasarkan data masukkan (input) yang digunakan. 
                        Terdapat 2 macam model yang digunakan untuk melatih (train) machine learning, setiap model memiliki 2 macam data masukkan yang dapat anda gunakan disesuaikan dengan kebutuhan anda.
                        \n\n**1. MLP - Text Processing** digunakan untuk data masukkan (input) berupa text, menggunakan Library Sklearn (MLPClassifier).
                        \n**2. MLP - Process File CSV** digunakan untuk data masukkan (input) berupa file CSV, menggunakan Library Sklearn (MLPClassifier).
                        \n**3. LSTM - Text Processing** digunakan untuk data masukkan (input) berupa text, menggunakan Library tensorflow.keras (LSTM).
                        \n**4. LSTM - Process File CSV** digunakan untuk data masukkan (input) berupa file CSV, menggunakan Library tensorflow.keras (LSTM).
                        \n\nKetentuan penggunanaan dapat anda lihat pada **Terms of service** di bawah.
                        \n\nAnda dapat membantu saya meningkatkan API ini, baik dengan membuat perubahan pada tampilan antarmuka maupun pada proses codingannya. Dengan begitu, saya dapat meningkatkan fitur - fitur lain pada API ini.
                        \nKritik dan saran silahkan hubungi melalui **Contact the developer** di bawah
                        \n\n\n_Referensi terkait Supervised Machine Learning (Data Classification) yang saya gunakan dapat anda cari [disini](https://github.com/prasamumtaz/23001027_14_PFM_API-Data-Cleaning_Challenge-Gold#readme)_
                        \n\nContoh file yang dapat digunakan:
                        \n- [Data](https://bit.ly/ContohData_Input)
                        \n\nDokumen lain yang digunakan pada proses **Cleaning**: 
                        \n- [New Kamus Alay](https://bit.ly/NewKamusAlay)
                        """,
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
@app.route('/1_MLP-text', methods=['POST'])
def text_processing_MLP():
    #request to input text
    text = request.form['text']

    #preprocessing text
    clean_text = dc.clean_text(text)
    #prediction
    sentiment = pred.text_prediction(clean_text, model='MLP')

    json_response = {
        'Sentiment': sentiment,
        'original_text': text,
        'clean_text': clean_text
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/MLP_processing_file.yml", methods=['POST'])
@app.route('/2_MLP-file-processing', methods=['POST'])
def upload_processing_file_MLP():

    #CSV File 
	#Upload single CSV File 
    file = request.files['file']
    #read CSV file
    df_fileInput = pd.read_csv(file, encoding='latin1')
    
    #preprocessing
    #Filter column Tweet column
    df_tweet= df_fileInput[['Tweet']]
    #apply data cleaning function from DataCleaning
    df_tweet['Tweet'] = df_tweet['Tweet'].apply(dc.clean_data)
    #Drop duplicates
    df_tweet= df_tweet.drop_duplicates()
    #Drop Missing Value
    df_tweet = df_tweet.dropna()

    #Prediction
    json_pred = pred.CSV_prediction(df_tweet, model='MLP', json_out=True)

    return json_pred

# ------------------------------------------- ENDPOINT LSTM ---------------------------------------------
@swag_from("docs/LSTM_text_processing.yml", methods=['POST'])
@app.route('/3_LSTM-text', methods=['POST'])
def text_processing_LSTM():
    #request to input text
    text = request.form['text']

    #preprocessing text
    clean_text = dc.clean_text(text)
    #prediction
    sentiment = pred.text_prediction(clean_text, model='LSTM')
    
    json_response = {
        'Sentiment': sentiment,
        'original_text': text,
        'clean_text': clean_text
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/LSTM_processing_file.yml", methods=['POST'])
@app.route('/4_LSTM-file-processing', methods=['POST'])
def upload_processing_file_LSTM():

    #CSV File 
	#Upload single CSV File 
    file = request.files['file']
    #read CSV file
    df_fileInput = pd.read_csv(file, encoding='latin1')
    
    #preprocessing
    #Filter column Tweet column
    df_tweet= df_fileInput[['Tweet']]
    #apply data cleaning fucntion from DataCleaning
    df_tweet['Tweet'] = df_tweet['Tweet'].apply(dc.clean_data)
    #Drop duplicates
    df_tweet= df_tweet.drop_duplicates()
    #Drop Missing Value
    df_tweet = df_tweet.dropna()

    #Prediction
    json_pred = pred.CSV_prediction(df_tweet, model='LSTM', json_out=True)

    return json_pred

if __name__ == '__main__':
   app.run()