from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import os
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

def predictions_page(request:HttpRequest):
    if request.method == "POST":
        body = request.POST
        # print(body)
        # <QueryDict: {'csrfmiddlewaretoken': ['IUmq7pBMh2YsD9GiaLW3Ao5Zyx60ncDk18TlhNybLEviRA5r3ynDdCCWrJmNt5zp'], 'analysis_type': ['classification'], 'file_id': ['a10bd100-c48b-467f-b2da-788f5dbfc400_test.csv']}>
        # print(body['file_id'])    # all the parameters are accessible

        baseDir:str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))        # get base dir name
        media_path:str = os.path.join(baseDir,'media')

        file_name:str = __getFile(media_path,body['file_id'])
        file_ext:str = file_name.split('.').pop()

        best_model:dict = __automlPipeline(pd.read_csv(file_name) if file_ext == "csv" else pd.read_excel(file_name), body['analysis_type'])

        os.remove(file_name)
        print(best_model)
        return render(request, 'automl_app/index.html', {'best_model': best_model})
        
    return render(request ,'automl_app/index.html')

def __getFile(mediaPath,fileName):
    for file in os.listdir(mediaPath):
        if fileName == file:
            return os.path.join(mediaPath, file)
    
    return None

def __automlPipeline(data:pd.DataFrame, analysis_type:str) -> dict:
    # fill null values in numeric columns
    data:pd.DataFrame = data.fillna(data.median(numeric_only=True))
    
    # Encode categorical features
    label_encoders:dict = {}
    for col in data.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
        label_encoders[col] = le

    X = data.iloc[:, :-1]  # All columns except the last one
    y = data.iloc[:, -1]   # The last column is the target

    # Standardize numeric features for large values
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models:dict = None
    scoring:str = None
    if analysis_type == "classification":
        models = {
            'LogisticRegression': {
                'model': LogisticRegression(),
                'params': {'C': [0.1, 1, 10], 'solver': ['lbfgs', 'liblinear']}     # here C represents the strength of Regularization(inverse)
            },
            'RandomForestClassifier': {
                'model': RandomForestClassifier(),
                'params': {'n_estimators': [5, 10, 20], 'max_depth': [None, 10]}
            },
            'SVC': {
                'model': SVC(),
                'params': {'C': [0.1, 1, 10], 'kernel': ['rbf', 'linear']}
            },
            'DecisionTreeClassifier': {
                'model': DecisionTreeClassifier(),
                'params': {'max_depth': [None, 10, 20], 'criterion': ['gini', 'entropy']}
            }
        }
        scoring = 'accuracy'
    else:
        models = {
            'LinearRegression': {
                'model': LinearRegression(),
                'params': {}
            },
            'RandomForestRegressor': {
                'model': RandomForestRegressor(),
                'params': {'n_estimators': [5, 10, 20], 'max_depth': [None, 10]}
            },
            'SVR': {
                'model': SVR(),
                'params': {'C': [0.1, 1, 10], 'kernel': ['rbf', 'linear']}
            },
            'DecisionTreeRegressor': {
                'model': DecisionTreeRegressor(),
                'params': {'max_depth': [None, 10, 20], 'criterion': ['mse', 'friedman_mse']}
            }
        }
        scoring = 'neg_mean_squared_error'

    # Apply GridSearchCV
    best_model = None
    best_score = -np.inf
    best_params = None

    for model_name, model_info in models.items():
        grid = GridSearchCV(estimator=model_info['model'], param_grid=model_info['params'], scoring=scoring, cv=5)
        grid.fit(X_train, y_train)
        score = grid.best_score_

        print(f"Model: {model_name}, Best Score: {score}, Best Params: {grid.best_params_}")
        if score > best_score:
            best_model = model_name
            best_score = score
            best_params = grid.best_params_

    # Test the best model on the test set
    final_model = models[best_model]['model'].set_params(**best_params)
    final_model.fit(X_train, y_train)

    y_pred = final_model.predict(X_test)
    if analysis_type == "classification":
        test_score = accuracy_score(y_test, y_pred)
    else:
        test_score = mean_squared_error(y_test, y_pred)

    # print("\nFinal Results:")
    # print(f"Best Model: {best_model}")
    # print(f"Best Score (Train): {best_score}")
    # print(f"Test Score: {test_score}")
    # print(f"Best Params: {best_params}")

    return {
        'best_model': best_model,
        'best_score_train': best_score,
        'test_score': test_score,
        'best_params': best_params
    }