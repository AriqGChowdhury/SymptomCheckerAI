import joblib
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

class Model:
    def __init__(self):
        self.sc_model = joblib.load('Symptom_Checker_Model.pkl')
        self.le = LabelEncoder()
        self.ohe = OneHotEncoder(sparse_output=False)
        self.df = pd.DataFrame()
        

    def get_user_input(self, user_input):
        
        user_input1 = {
            'Fever': user_input['Fever'],
            'Cough': user_input['Cough'],
            'Fatigue': user_input['Fatigue'],
            'Difficulty Breathing': user_input['Difficulty Breathing'],
            'Age': user_input['Age'],
            'Gender': user_input['Gender'],
            'Outcome Variable': user_input['Outcome Variable'],
            'Blood Pressure': user_input['Blood Pressure'],
            'Cholesterol Level': user_input['Cholesterol Level'],
        }
        
        

        user_df = pd.DataFrame([user_input1])
        ohe_transform = self.ohe.fit_transform(user_df[['Blood Pressure', 'Cholesterol Level']])
        ohe_df = pd.DataFrame(ohe_transform, columns=self.ohe.get_feature_names_out(['Blood Pressure', 'Cholesterol Level']))

        user_df['Gender'] = self.le.fit_transform(user_df['Gender'])
        user_df['Cough'] = self.le.fit_transform(user_df['Cough'])
        user_df['Difficulty Breathing'] = self.le.fit_transform(user_df['Difficulty Breathing'])
        user_df['Fever'] = self.le.fit_transform(user_df['Fever'])
        user_df['Fatigue'] = self.le.fit_transform(user_df['Fatigue'])
        user_df['Outcome Variable'] = self.le.fit_transform(user_df['Outcome Variable'])
        user_df = user_df.drop(columns=['Blood Pressure', 'Cholesterol Level']).reset_index(drop=True)
        user_df = pd.concat([user_df, ohe_df], axis=1)
        bp_chol = ['Blood Pressure_High', 'Blood Pressure_Low', 'Blood Pressure_Normal', 'Cholesterol Level_High', 'Cholesterol Level_Low', 'Cholesterol Level_Normal']
        for columns in self.ohe.get_feature_names_out(['Blood Pressure', 'Cholesterol Level']):
            bp_chol.remove(columns)
        for columns in bp_chol:
            user_df[columns] = 0.0
        user_df = user_df[['Fever', 'Cough', 'Fatigue', 'Difficulty Breathing', 'Age', 'Gender', 'Outcome Variable', 'Blood Pressure_High', 'Blood Pressure_Low', 'Blood Pressure_Normal', 'Cholesterol Level_High', 'Cholesterol Level_Low', 'Cholesterol Level_Normal']]
        return self.sc_model.predict(user_df).tolist()