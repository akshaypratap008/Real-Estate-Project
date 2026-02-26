import sys
import os
from dataclasses import dataclass

import pandas as pd
import numpy as np
import sklearn

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from category_encoders import TargetEncoder

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
            cat_columns_ohe = ['property_type', 'balcony', 'agePossession', 'furnishing_type', 'luxury_category', 'floor_category']       #one hot encoding
            cat_columns_ord = ['agePossession', 'furnishing_type']  #ordinal encoding
            cat_columns_te = ['sector']     #target encoding
            num_columns = ['bedRoom', 'bathroom', 'built_up_area', 'servant room', 'store room']

            preprocessor = ColumnTransformer(
                    [
                    ('ordinal_encoding', OrdinalEncoder(), cat_columns_ord),
                    ('standard_scaling', StandardScaler(), num_columns),
                    ('ohe', OneHotEncoder(handle_unknown='ignore'), cat_columns_ohe),
                    ('target_encoding', TargetEncoder(), cat_columns_te)
                ], remainder='passthrough'
            )

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
            input_feature_train_df['built_up_area'] = np.log1p(input_feature_train_df['built_up_area'])
            target_feature_train_df = train_df[target_column]

            
            #test_df
            input_feature_test_df = test_df.drop(columns = [target_column])
            input_feature_test_df['built_up_area'] = np.log1p(input_feature_test_df['built_up_area'])
            target_feature_test_df = test_df[target_column]

            # target column transformation
            target_feature_train_df = np.log1p(train_df[target_column])
            target_feature_test_df = np.log1p(test_df[target_column])

            # column transformation on train and test set
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df, target_feature_train_df)      # targetEncoder needs both X and y to fit
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
 
            # concat input_feature and taget feature for train and test respectively
            train_arr = np.c_[input_feature_train_arr, target_feature_train_df]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_df]

            logging.info('train and test array prepared')

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path, 
                obj = preprocessing_obj
            )

            logging.info('preprocessing object saved in directory')
            return (
                train_arr, 
                test_arr, 
                self.data_transformation_config.preprocessor_obj_file_path
            )  

        except Exception as e:
            raise CustomeException(e, sys)


