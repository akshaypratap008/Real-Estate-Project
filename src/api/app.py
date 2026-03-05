from fastapi import FastAPI
from src.api.schemas import UserInput
import pandas as pd
from src.pipelines.predict_pipeline import PredictPipeline
from fastapi.responses import JSONResponse
from src.exceptions import CustomeException
from src.logger import logging
import sys

app = FastAPI()

@app.post('/predict')
def make_prediction(user_input: UserInput):
    try:
        input_df = pd.DataFrame([{
            'property_type': user_input.property_type,
            'sector': user_input.sector,
            'bedRoom': user_input.bedroom,
            'bathroom': user_input.bathroom,
            'balcony': user_input.balcony,
            'agePossession': user_input.agePossession,
            'built_up_area': user_input.built_up_area,
            'servant room': user_input.servant_room,
            'store room': user_input.store_room,
            'furnishing_type': user_input.furnishing_type,
            'luxury_category': user_input.luxury_category,
            'floor_category': user_input.floor_category
        }])
        logging.info('Input data validated using pydantic and converted into dataframe object')

        model = PredictPipeline()
        prediction = model.predict(input_df)[0]

        logging.info('Prediction pipeline successfully run')
        return JSONResponse(status_code=200, content = f'Predicted price of the property is {prediction}')
    except Exception as e:
        raise CustomeException(e, sys)

