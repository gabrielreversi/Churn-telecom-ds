from sklearn.model_selection import train_test_split
from imblearn.under_sampling import RandomUnderSampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib



class TrainModel:

    def __init__(self, dataframe):
        self.dataframe = dataframe

    
    def split_dataframe(self):

        x = self.dataframe.drop(['Churn','customerID'], axis=1)
        y = self.dataframe['Churn']

        X_train, X_test, y_train, y_test = train_test_split(x, y, stratify=y, shuffle=True)

        spl = RandomUnderSampler()
        x_train_res, y_train_res = spl.fit_resample(X_train, y_train)

        return x_train_res, y_train_res, X_test, y_test
    
    def apply_randomforest(self, x_train, y_train, x_test, y_test):

        self.randomF = RandomForestClassifier(
            criterion='entropy',
            random_state=0,
            min_samples_leaf= 10,
            min_samples_split=10,
            n_estimators=150)
        
        self.randomF.fit(x_train, y_train)

        randomF_predict = self.randomF.predict(x_test)
        result = accuracy_score(y_test, randomF_predict)

        return result
    
    def save_model(self):
        joblib.dump(self.randomF, "D:/Env-projects-ds/Churn-telecom-ds/src/churn_telecom/model/random_forest.joblib")


