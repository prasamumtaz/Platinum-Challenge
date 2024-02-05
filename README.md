# Binar Platinum Challenge
## Tentang API
![Alt text](image\API.png)
Proses pembuatan API menggunakan flask untuk mempermudah pembuatan web app dan Swagger UI untuk membantu membuat tampilan antar-muka dokumentasi (docs). Pada API ini terdapat 4 endpoint yaitu:
> 1. **MLP - Text Processing** digunakan untuk menghasilkan output sentiment (negative, neutral, positif) yang dihasilkan dari `model basic Neural Network (MLP)` dengan masukkan (input) berupa string 
![alt text](image\MLP_text.png)
> 1. **MLP - Process File CSV** digunakan untuk menghasilkan output sentiment (negative, neutral, positif) yang dihasilkan dari `model basic Neural Network (MLP)` dengan masukkan (input) berupa CSV file 
![alt text](image\MLP_CSV.png)
> 1. **LSTM - Text Processing** digunakan untuk menghasilkan output sentiment (negative, neutral, positif) yang dihasilkan dari `model LSTM` dengan masukkan (input) berupa string 
![alt text](image\LSTM_text.png)
> 1. **LSTM - Process File CSV** digunakan untuk menghasilkan output sentiment (negative, neutral, positif) yang dihasilkan dari `model LSTM` dengan masukkan (input) berupa CSV file 
![alt text](image\LSTM_CSV.png)
## Daftar Folder & File
Selain API, terdapat 3 folder yang digunakan untuk proses pembuatan `model basic Neural Network (MLP) dan LSTM`
- Data_Cleaning_Notebook
- Neural_Network_MPL
- Neural_Network_LSTM

> 3 folder file di atas berisikan file yang digunakan untuk mebuat model basic Neural Network (MLP) dan LSTM

### Dalam Folder API
- Folder **Data_For_DataCleaning** merupakan folder yang berisi file .csv dan .txt untuk keperluan program **DataCleaning.py**
- Folder **DataBase** merupakan folder yang digunakan untuk menyimpan seluruh data pre dan pasca processing menggunakan API
- Folder **docs** merupakan folder yang berisi template Swagger UI
    > **MLP_text_processing.yml** template yang digunakan untuk endpoint **MLP - Text Processing**

    > **MLP_processing_file.yml** template yang digunakan untuk endpoint **MLP - Process File CSV**

    > **LSTM_text_processing.yml** template yang digunakan untuk endpoint **LSTM - Process File CSV**
    
    > **LSTM_processing_file.yml** template yang digunakan untuk endpoint **LSTM - Process File CSV**

- **app.py** adalah program untuk menjalankan API
- **DataCleaning.py** merupakan file python  yang digunakan untuk `proses cleaning` di dalam program API
- **Prediction.py** merupakan file python  yang digunakan untuk `proses prediksi sentiment` di dalam program API

### Informasi lain terkait proses pembuatan model dan API dapat dilihat pada file [Report Kelompok 1](https://github.com/prasamumtaz/Platinum-Challenge/blob/main/Report%20Kelompok%201.pdf)