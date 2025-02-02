import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler#, MinMaxScaler
from transformer import DateTransform, AgeTransform,CodeCountTransform,CodeFrequencyGroupTransform
from transformer import Top15OneHotTransform,ProviderLevelAggregateTransform
import numpy as np
from sklearn.model_selection import train_test_split

class Fraud_Detector(object):
    def __init__(self):
        pass
    def build_model(self):
        """
        Building model pipeline 
        """
        steps = [#('preprocessor',preprocessor),
        ('rescale', StandardScaler()),
        #('rescale', MinMaxScaler()),
        ('clf', LogisticRegression(class_weight ='balanced',C=0.01,random_state=67, max_iter=10000))]
        self.pipeline = Pipeline(steps)
    def train(self):
        """
        Train a model 
        """
        # load the data from csv to pandas dataframe
        X_train_aggregated_raw = pd.read_csv("data/X_train.csv")
        y_train_aggregated_raw = pd.read_csv("data/y_train.csv")

        # Define feature and target 
        target = ["Provider", "PotentialFraud"]
        features = list(X_train_aggregated_raw.columns)
        self.features = [fea for fea in features if fea not in target]

        y_train=y_train_aggregated_raw['PotentialFraud']
        X_train=X_train_aggregated_raw.drop('Provider',axis=1).fillna(0)

        self.build_model()
        self.model = self.pipeline.fit(X_train, y_train)
    
    def predict(self, context):
        """
        context: dictionary format {'TotalTEDiagCode':502,... etc}
        return np.array
        """
        num_predictions = len([context[self.features[0]]])
        print(num_predictions)
        X = pd.DataFrame(context,index=range(num_predictions))
        return self.model.predict_proba(X)

class Fraud_Detector_RF8(object):
    def __init__(self):
        pass
    def build_model(self):
        """
        Building model pipeline 
        """
        steps = [#('preprocessor',preprocessor),
        # ('rescale', StandardScaler()),
        #('rescale', MinMaxScaler()),
        ('clf', RandomForestClassifier(max_depth = 20, min_samples_split = 8, n_estimators =700, class_weight = 'balanced', random_state = 42))]
        self.pipeline = Pipeline(steps)
    def train(self):
        """
        Train a model 
        """
        # load the data from csv to pandas dataframe
        X_train_aggregated_raw = pd.read_csv("data/X_train.csv")
        y_train_aggregated_raw = pd.read_csv("data/y_train.csv")

        # Define feature and target 
        target = ["Provider", "PotentialFraud"]
        features = ['MaxHospitalDays',
                    'TotalInscClaimAmtReimbursed',
                    'TotalIPAnnualReimbursementAmt',
                    'MaxInscClaimAmtReimbursed',
                    'MaxDiagCodeNumPerClaim',
                    'TotalDiagCodeNum',
                    'MaxProcCodeNumPerClaim',
                    'MeanProcCodeNumPerClaim']
        self.features = [fea for fea in features if fea not in target]

        y_train=y_train_aggregated_raw['PotentialFraud']
        X_train=X_train_aggregated_raw[features].fillna(0)

        self.build_model()
        self.model = self.pipeline.fit(X_train, y_train)
    
    def predict(self, context):
        """
        context: dictionary format {'MaxProcCodeNumPerClaim': 0, 'MeanProcCodeNumPerClaim': 0.0,... etc}
        return np.array
        """
        num_predictions = len([context[self.features[0]]])
        print(num_predictions)
        X = pd.DataFrame(context,index=range(num_predictions))
        return self.model.predict_proba(X)