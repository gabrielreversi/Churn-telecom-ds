

from ..data.azure_connection import AzureCon


server = "server_name"
database = "study-sql"
username = "user_name"
password = "psd"
driver = '{ODBC Driver 18 for SQL Server}'

connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

con = AzureCon()

df = con.connection_az(connection_string)