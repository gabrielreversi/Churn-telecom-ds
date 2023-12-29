import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


class Processing:

    def __init__(self, dataframe):
        self.dataframe = dataframe


    def handle_null(self):
        try:
            self.dataframe["TotalCharges"] = self.dataframe["TotalCharges"].replace(' ', np.nan).astype(float)
            self.dataframe['TotalCharges'].replace(np.nan, self.dataframe["TotalCharges"].median(), inplace=True)
          
            return self.dataframe
        
        except Exception as e:
            print(f"Erro ao converter valores. {e}")

    def preprocess(self, X):
        df_output = self.dataframe.copy()
        
        for col in df_output.select_dtypes('object').columns:
            lb = LabelEncoder()
            df_output[col] = lb.fit_transform(df_output[col])
        for col in df_output.select_dtypes('float').columns:
            sd = StandardScaler()
            df_output[col] = sd.fit_transform(df_output[col].values.reshape(-1,1))
        
        return df_output
    
    def pipeline_sk(self):
        steps = [
            ('preprocess', FunctionTransformer(self.preprocess))
        ]
        pipe = Pipeline(steps)

        return pipe

