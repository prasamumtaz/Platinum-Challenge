import re

from flask import Flask, jsonify
import pandas as pd
from flask import request
import flask
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
import sqlite3

app = Flask(__name__)

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title' : "Challenge 1 API Documentation for Data Processing and Modeling by Fachry",
        'version' : "1.0.0",
        'description' : "Dokumentasi API untuk Data Processing dan Modeling",
    },
    host = "127.0.0.1:5000/"
)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint":"docs",
            "route" : "/docs.json",
        } 
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template, config = swagger_config)

@swag_from("docs/text_processing.yml", methods = ['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():
    text = request.form.get('text')
    if text:
        # Apply the desired text cleaning operations
        text = re.sub(r'\bUSER\b', '', text)
        text = re.sub(r'RT:', '', text)
        text = re.sub(r'rt', '', text)
        text = re.sub(r'\\x[0-9a-f]{2}', '', text)
        text = re.sub(r'[^A-Za-z0-9\s]+', '', text)
        text = re.sub(r'x[0-9a-fA-F]+', '', text)
        text = re.sub(r'http\S+|www.\S+', '', text)
        text = re.sub(r'\s+', ' ', text)

        description = "Teks yang sudah diproses"
        try: 
            conn = sqlite3.connect('D:\Challenge Topic 3 DSC\database_challenge.db') 
            cursor = conn.cursor() 
            cursor.execute("INSERT INTO results_api (description, data) VALUES (?, ?)", (description, text))
            conn.commit()
        except Exception as e: 
            return jsonify({'status_code': 500, 'description': str(e)}), 500 
        finally: 
            conn.close()

        

        json_response = {
            'status_code': 200,
            'description': "Teks yang sudah diproses",
            'data': text,
        }
    else:
        json_response = {
            'status_code': 400,
            'description': "No text data provided",
        }
    response_data = jsonify(json_response)
    return response_data

def text_cleaning(text):
    # Text cleaning using regular expressions
    text = re.sub(r'\bUSER\b', '', text)
    text = re.sub(r'RT:', '', text)
    text = re.sub(r'rt', '', text)
    text = re.sub(r'\\x[0-9a-f]{2}', '', text)
    text = re.sub(r'[^A-Za-z0-9\s]+', '', text)
    text = re.sub(r'x[0-9a-fA-F]+', '', text)
    text = re.sub(r'http\S+|www.\S+', '', text)
    text = re.sub(r'\s+', ' ', text)

    return text

@swag_from("docs/file_upload.yml", methods = ['POST'])
@app.route('/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    try:
        db_connection=sqlite3.connect('D:\Challenge Topic 3 DSC\database_challenge.db', check_same_thread=False)
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file, encoding='latin1')

        # Apply text cleaning to the DataFrame
        df['Tweet'] = df['Tweet'].apply(text_cleaning)

        # Save the cleaned DataFrame to sqlite
        df.to_sql('results_api2', db_connection, if_exists='replace', index=False)
        db_connection.commit()

        # Convert the cleaned DataFrame to a JSON response
        response_data = df.to_json(orient='records')
        return jsonify({'status_code': 200, 'description': 'CSV file cleaned successfully', 'data': response_data})

    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        db_connection.close()

if __name__ == '__main__':
    app.run()




















