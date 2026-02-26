import os
import sys

import numpy as np

from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_absolute_error

from src.logger import logging
from src.exceptions import CustomeException
from src.components.data_transformation import DataTransformationConfig
from src.utils import evaluate_models, save_object
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

           model = RandomForestRegressor()
           
           grid_param = {
            'n_estimators': [250, 300, 350],
            'criterion': ['squared_error'],   
            'max_depth': [25, 30, 35],
            'min_samples_split': [2, 3, 4],
            'min_samples_leaf': [1, 2],
            'max_features': [None, 'sqrt']
            }
           
           train_mae_score, test_mae_score, best_model = evaluate_models(model, grid_param, X_train, y_train, X_test, y_test)

           save_object(
               file_path=self.model_trainer_config.trained_model_file_path,
               obj = best_model
           )
           
           logging.info('model pickle file saved in artifacts folder')

           return (train_mae_score, test_mae_score)
        
        except Exception as e:
            raise CustomeException(e, sys)