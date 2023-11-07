
import pyodbc
import pandas as pd

class AzureCon:

    def connection_az(self, connection_string):
        try:
            conn = pyodbc.connect(connection_string)
            query = "select * from [dbo].[Telecom-churn]"
            df = pd.read_sql(query, conn)
        except pyodbc.Error as e:
            print("Erro ao conectar ao Azure SQL Database:", e)
        finally:
            conn.close()

        return df

    