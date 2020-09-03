from xgboost import XGBClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

import pandas as pd
import joblib


def train(data_conf, model_conf, **kwargs):
    hyperparams = model_conf["hyperParameters"]

    column_names = ["NumTimesPrg", "PlGlcConc", "BloodP", "SkinThick", "TwoHourSerIns", "BMI", "DiPedFunc", "Age", "HasDiabetes"]
    dataset = pd.read_csv(data_conf['url'], header=None, names=column_names)

    # split into test and train
    train, _ = train_test_split(dataset, test_size=data_conf["test_split"], random_state=42)

    # split data into X and y
    train = train.values
    X_train = train[:, 0:8]
    y_train = train[:, 8]

    print("Starting training...")

    # fit model to training data
    model = Pipeline([('scaler', MinMaxScaler()),
                     ('xgb', XGBClassifier(eta=hyperparams["eta"],
                                           max_depth=hyperparams["max_depth"]))])
    # xgboost saves feature names but lets store on pipeline for easy access
    model.feature_names = column_names[0:8]

    model.fit(X_train, y_train)

    print("Finished training")

    # export model artefacts
    joblib.dump(model, "artifacts/output/model.joblib")

    print("Saved trained model")
