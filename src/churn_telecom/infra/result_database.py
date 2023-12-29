




class SaveNewData:

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def save_data(self, table_name, data):

        # Inserir os dados na tabela do Azure SQL
        for index, row in data.iterrows():
            values = "','".join(map(str, row.values))
            insert_query = f"INSERT INTO {table_name} VALUES ('{values}')"
            self.cursor.execute(insert_query)

        # Commit e fechar a conexão
        self.conn.commit()
        self.conn.close()

    def delete_data(self, table_name):

        try:
            delete_query = f"DELETE FROM {table_name}"

            # Executar o comando SQL
            self.cursor.execute(delete_query)

            # Commit e fechar a conexão
            self.conn.commit()
            print(f'Todas as linhas da tabela {table_name} foram excluídas com sucesso.')

        except Exception as e:
            print(f"Erro ao excluir linhas da tabela {table_name}: {e}")

