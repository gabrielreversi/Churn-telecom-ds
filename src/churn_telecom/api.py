# Importar as bibliotecas necessárias
from fastapi import FastAPI, File, UploadFile, status, Response
import pandas as pd
import joblib
import uvicorn
import io
from data.preprocess.pipeline_preprocess import Processing
from infra.azure_connection import connection_az
from infra.result_database import SaveNewData
from config import azure_db_connection
import json

# Criar uma instância do FastAPI
app = FastAPI()

# Carregar o modelo salvo
model = joblib.load("D:/Env-projects-ds/Churn-telecom-ds/src/churn_telecom/model/random_forest.joblib")

# Definir uma rota para o endpoint
@app.post("/predict", status_code=status.HTTP_200_OK)
async def predict(file: UploadFile = File(...)):
    try:
        # Receber o arquivo csv enviado pelo usuário
        contents = await file.read()
        # Converter o objeto bytes em um objeto StringIO
        contents = io.StringIO(contents.decode("utf-8"))
        # Converter o arquivo em um dataframe
        df = pd.read_csv(contents)

        processing = Processing(df)
        # Aplicar o pipeline de processamento
        x = processing.pipeline_sk().fit_transform(df)
        # Fazer a predição usando o modelo
        prediction = model.predict(x)
        # Retornar a predição em formato JSON
        return Response(status_code=status.HTTP_200_OK, content=json.dumps({"prediction": prediction.tolist()}), media_type="application/json")
    except Exception as e:
        error_message = f"An error ocurred: {str(e)}"
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error":error_message})

@app.delete("/delete_all_data", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all(
    table_name:str
):
    try:
        connection = connection_az(connect_database=azure_db_connection)
        save_methd = SaveNewData(connection)
        save_methd.delete_data(table_name=table_name)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error_message = f"An error ocurred: {str(e)}" 
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error":error_message})
    
@app.post("/predict_and_save", status_code=status.HTTP_200_OK)
async def predict_and_save(file: UploadFile = File(...)):
    try:
        # Receber o arquivo csv enviado pelo usuário
        contents = await file.read()
        # Converter o objeto bytes em um objeto StringIO
        contents = io.StringIO(contents.decode("utf-8"))
        # Converter o arquivo em um dataframe
        df = pd.read_csv(contents)

        # Fazer a previsão
        processing = Processing(df)
        x = processing.pipeline_sk().fit_transform(df)
        prediction = model.predict(x)

        # Adicionar a coluna 'churn' com os resultados da previsão
        df['churn'] = prediction.tolist()

        # Salvar no banco de dados
        connection = connection_az(connect_database=azure_db_connection)
        save_methd = SaveNewData(connection)
        save_methd.save_data(table_name="Telecom_churn_newdata", data=df)

        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=json.dumps({"error": error_message}), media_type="application/json")








