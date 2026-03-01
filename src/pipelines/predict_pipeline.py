import sys
import pandas as pd

from src.utils import load_object
from src.exceptions import CustomeException
from src.logger import logging

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, input_data):
        try:
            preprocessor = load_object(r'C:\Users\apaks\Desktop\Real Estate Project\artifacts\preprocessor.pkl')

            model = load_object(r'C:\Users\apaks\Desktop\Real Estate Project\artifacts\model.pkl')
            logging.info('model and preprocessor object loaded')

            input_data_preprocessed = preprocessor.transform(input_data)
            logging.info('input data preprocessing completed')

            prediction = model.predict(input_data_preprocessed)
            logging.info('prediction output generated')

            return prediction
        
        except Exception as e:
            raise CustomeException(e, sys)

class CustomData:
    def __init__(
            self, 
            property_type:str, 
            sector:str, 
            bedroom:int, 
            bathroom:int, 
            balcony:str, 
            agePossession:str, 
            built_up_area:float, 
            servant_room:int, 
            store_room:int, 
            furnishing_type:str, 
            luxury_category:str, 
            floor_category:str
            ):
        
        self.property_type = property_type
        self.sector = sector
        self.bedroom = bedroom
        self.bathroom = bathroom
        self.balcony = balcony
        self.agePossession = agePossession
        self.built_up_area = built_up_area
        self.servant_room = servant_room
        self.store_room = store_room
        self.furnishing_type = furnishing_type
        self.luxury_category = luxury_category
        self.floor_category = floor_category

    def get_data_as_df(self):
        try:
            input_data_dict = {
                    'property_type': self.property_type,
                    'sector': self.sector,
                    'bedRoom': self.bedroom,
                    'bathroom': self.bathroom,
                    'balcony': self.balcony,
                    'agePossession': self.agePossession,
                    'built_up_area': self.built_up_area,
                    'servant room': self.servant_room,
                    'store room': self.store_room,
                    'furnishing_type': self.furnishing_type,
                    'luxury_category': self.luxury_category,
                    'floor_category': self.floor_category
            }

            logging.info('input data converted into dataframe')
            return pd.DataFrame([input_data_dict])
        
        except Exception as e:
            raise CustomeException(e, sys)



        