import os
import sys

from src.exceptions import CustomeException
from src.logger import logging
from src.components.data_transformation import DataTransformationConfig, DataTransformation
from src.components.model_trainer import ModelTrainerConfig, ModelTrainer

import pandas as pd
from sklearn.model_selection import train_test_split

from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    raw_data_path = os.path.join('artifacts', 'data.csv')
    train_data_path = os.path.join('artifacts', 'train.csv')
    test_data_path = os.path.join('artifacts', 'test.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('entered the data ingestion component')
        try:
            df = pd.read_csv(r'artifacts\data\preprocessed-data\gurgaon_properties_post_feature_selection.csv')
            logging.info('file exported as dataframe')

            # save raw data
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index = False, header=True)
            logging.info('raw data saved')

            # train test split
            train_set, test_set = train_test_split(df, test_size=0.2, random_state = 42)
            train_set.to_csv(self.ingestion_config.train_data_path, index = False, header = True)
            test_set.to_csv(self.ingestion_config.test_data_path, index = False, header = True)
            logging.info('data ingestion completed')

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomeException(e, sys)
        
if __name__ == '__main__':
    obj = DataIngestion()
    train_path, test_path = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_path, test_path)

    modeltrainer = ModelTrainer()
    modeltrainer.initiate_model_training(train_arr, test_arr)