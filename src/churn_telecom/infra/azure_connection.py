
import pyodbc

def connection_az(connect_database):
        
        try:
            conn = pyodbc.connect(connect_database)

            return conn
        
        except pyodbc.Error as e:
            
            return print("Erro ao conectar ao Azure SQL Database:", e)
        #finally:
        #    conn.close()
    

