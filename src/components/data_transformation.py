import sys
import os
from dataclasses import dataclass

import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, TargetEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from src.exceptions import CustomeException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def build_processor_object(self):
        # function converts different columns to appropriate encoding
        try:
            cat_columns_to_encode = ['property_type', 'sector', 'balcony', 'agePossession', 'furnishing_type', 'luxury_category', 'floor_category']

            num_columns_to_encode = ['bedRoom', 'bathroom', 'built_up_area', 'servant room', 'store room']

            cat_columns_to_ohe = ['agePossession', 'furnishing_type'] 

            cat_column_to_target_encode = ['sector']

            preprocessor = ColumnTransformer([
                ('cat_col_encoding', OrdinalEncoder(), cat_columns_to_encode),
                ('num_col_to_encode', StandardScaler(), num_columns_to_encode),
                ('cat_col_to_ohe', OneHotEncoder, cat_columns_to_ohe),
                ('cat_col_to_target_encode', TargetEncoder(), cat_column_to_target_encode)
            ], remainder = 'passthrough')

            logging.info('Column encoding complete')

            return preprocessor
        
        except Exception as e:
            raise CustomeException(e, sys)
            

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('train and test data pulled from file and saved as dataframe')

            logging.info('obtaining preprocessor object')

            preprocessing_obj = self.build_processor_object()

            target_column = 'price'

            #train df
            input_feature_train_df = train_df.drop(columns = [target_column])
            target_feature_train_df = train_df['price']
            
            #test_df
            input_feature_test_df = test_df.drop(columns = [target_column])
            target_feature_test_df = test_df[target_column]

            logging.info('train and test set split into input feature and target feature')

            # apply transformations on X and y
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.fit_transform(input_feature_test_df)

            target_feature_train_df = np.log1p(target_feature_train_df)     # log transformation of target feature 'price'

            # concat input_feature and taget feature for train and test respectively
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info('train and test array prepared')

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path, 
                obj = preprocessing_obj
            )

            logging.info('train and test array and preprocessing object saved in directory')
            return (
                train_arr, 
                test_arr, 
                self.data_transformation_config.preprocessor_obj_file_path
            )  

        except:
            pass


