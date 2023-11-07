

from ..data.azure_connection import AzureCon


server = "study-server-sql.database.windows.net"
database = "study-sql"
username = "gabrieladmin"
password = "Grc@5129788"
driver = '{ODBC Driver 18 for SQL Server}'

connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

con = AzureCon()

df = con.connection_az(connection_string)
print(df.head())
