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
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok= True)
        
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomeException(e, sys)
    
def evaluate_models(model, grid_param:dict, X_train, y_train, X_test, y_test):
    try:        
        model = RandomForestRegressor()
                
        kfold = KFold(n_splits=10, shuffle=True, random_state=42)
        search = RandomizedSearchCV(model, grid_param, n_iter=30, scoring='r2', cv = kfold, verbose=2, n_jobs=-1, random_state=42)
        logging.info('Model Training started')
        search.fit(X_train, y_train)
        
        logging.info('best model found')
        best_model = search.best_estimator_
        best_score = search.best_score_      
        logging.info('new parameters fit on training data')

        y_train_pred = best_model.predict(X_train)
        y_test_pred = best_model.predict(X_test)

        train_mae_score = mean_absolute_error(y_train, y_train_pred)
        test_mae_score = mean_absolute_error(y_test, y_test_pred)

        logging.info('train and test score calculated')

        print('mae_train: ', train_mae_score)
        print('mae_test: ', test_mae_score)
        print('best_cv_r2_score: ', search.best_score_)
        return train_mae_score, test_mae_score, best_model

    except Exception as e:
        raise CustomeException(e, sys)
    
def load_object(file_path):
    try:
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except Exception as e:
        raise CustomeException(e, sys)



    