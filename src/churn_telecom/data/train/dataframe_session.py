import pandas as pd


class DataFrameCreate:

    def __init__(self, connect):
        self.connect = connect

    def create_dataframe(self):
        query = "select * from [dbo].[Telecom-churn]"
        df = pd.read_sql(query, self.connect)

        return df