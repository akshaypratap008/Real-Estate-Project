import os
import sys

import pandas as pd
import numpy as np

import dill
import pickle

from src.exceptions import CustomeException
from src.logger import logging

from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import cross_val_score, KFold, RandomizedSearchCV
from sklearn.pipeline import Pipeline

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok= True)
        
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomeException(e, sys)
    
def evaluate_models(models:dict, params_grid:dict, X_train, y_train, X_test, y_test):
    try:
        scores = {}

        for model_name, model in models.items():
            
            pipeline = Pipeline([
                ('regressor', model)
            ])

            kfold = KFold(n_splits=10, shuffle= True, random_state=42)
            search = RandomizedSearchCV(estimator=pipeline, param_distributions=params_grid[model_name],scoring='r2', n_iter=20 ,cv = kfold, n_jobs = -1, verbose = 1, random_state=42)

            search.fit(X_train, y_train)
            best_model = search.best_estimator_
            y_pred = best_model.predict(X_test)

            r2 = r2_score(np.expm1(y_test), np.expm1(y_pred))
            mae = mean_absolute_error(np.expm1(y_test), np.expm1(y_pred))

            scores[model_name] = {
                'best_params': search.best_params_,
                'cv_r2': search.best_score_,
                'r2': r2,
                'mae': mae
            }

        return scores

    except:
        pass


    