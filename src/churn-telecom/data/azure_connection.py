
import pyodbc
import pandas as pd

server = "SERVER_NAME.database.windows.net"
database = "DATABASE_NAME"
username = "USER"
password = "PWD"
driver = '{ODBC Driver 18 for SQL Server}'

connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'


class AzureCon:

    def connection_az(connection_string):
        conn = pyodbc.connect(connection_string)

        query = "select * from [dbo].[Telecom-churn]"

        df = pd.read_sql(query, conn)

        conn.close()

        return df
    