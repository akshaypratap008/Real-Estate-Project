import os
import sys

import numpy as np

from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_absolute_error

from src.logger import logging
from src.exceptions import CustomeException
from src.components.data_transformation import DataTransformationConfig
from src.utils import evaluate_models
from dataclasses import dataclass


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts', 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_training(self, train_arr, test_arr):
        try:
           # train and test data
           X_train, y_train, X_test, y_test = train_arr[:, :-1], train_arr[:, -1], test_arr[:, :-1], test_arr[:, -1]

           models = {
               'random_forest': RandomForestRegressor(),
               'xgb': XGBRegressor()
           }
           
           params_grid = {
                'random_forest': {
                    'regressor__n_estimators': [200, 300, 400],
                    'regressor__max_depth': [10, 20, 40, 50],
                    'regressor__min_samples_split': [2, 5, 7],
                    'regressor__min_samples_leaf': [1,2,3],
                    'regressor__max_features': ['sqrt', 'log2']
                },
                'xgb': {
                    'regressor__n_estimators': [200, 400, 500],
                    'regressor__learning_rate': [0.05, 0.08, 0.1],
                    'regressor__max_depth': [3, 5, 7],
                    'regressor__subsample': [0.8, 1.0],
                    'regressor__colsample_bytree': [0.8, 1.0],
                    'regressor__gamma': [0, 1, 2],
                    'regressor__min_child_weight': [1, 3, 5]
                }
            }
           

           scores = evaluate_models(models, params_grid, X_train, y_train, X_test, y_test)  
           print(scores)             

            # X_train, y_train, X_test, y_test = train_arr[:, :-1], train_arr[:, -1], test_arr[:, :-1], test_arr[:, -1]
            # model = XGBRegressor()

            # model.fit(X_train, y_train)
            # y_pred = model.predict(X_test)
            # r2 = r2_score(np.expm1(y_test), np.expm1(y_pred))
            # mae = mean_absolute_error(np.expm1(y_test), np.expm1(y_pred))

            # print('r2_score: ', r2)  
            # print('mae: ', mae)
        except Exception as e:
            raise CustomeException(e, sys)