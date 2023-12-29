from infra.azure_connection import connection_az
from data.train.dataframe_session import DataFrameCreate
from data.preprocess.pipeline_preprocess import Processing
from data.train.training import TrainModel
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:study-server-sql.database.windows.net,1433;Database=study-sql;Uid=gabrieladmin;Pwd={Grc@5129788};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
connection = connection_az(string)
call_cls = DataFrameCreate(connection)
df = call_cls.create_dataframe()


# Criar uma instância da classe Processing e passar o dataframe
get_dataframe = Processing(dataframe=df)
# Chamar o método handle_null
get_dataframe.handle_null()
# Chamar o método pipeline_sk
pipe = get_dataframe.pipeline_sk()
# Usar o método fit_transform da pipeline
x = pipe.fit_transform(get_dataframe.dataframe)
# Converter o array numpy em um dataframe
x = pd.DataFrame(x, columns=get_dataframe.dataframe.columns)


#split dataframe
training = TrainModel(dataframe=x)
x_train_res, y_train_res, X_test, y_test = training.split_dataframe()

#train model
result_model = training.apply_randomforest(x_train=x_train_res,
                                           y_train=y_train_res,
                                           x_test=X_test,
                                           y_test=y_test)

save = training.save_model()

# Imprimir o dataframe
print(result_model)