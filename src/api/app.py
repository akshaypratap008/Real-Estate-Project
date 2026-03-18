from fastapi import FastAPI
from src.api.schemas import UserInput, PredictionResponse, ExplainationResponse
import pandas as pd
from src.pipelines.predict_pipeline import PredictPipeline
from fastapi.responses import JSONResponse
from src.exceptions import CustomeException
from src.logger import logging
import sys
import joblib
import shap

app = FastAPI()

MODEL_VERSION = '1.0.0'
model = PredictPipeline()

# load model and preprocessor directly for SHAP 
rf_model = joblib.load("artifacts\model.pkl")
preprocessor = joblib.load("artifacts\preprocessor.pkl")

def user_input_to_df(user_input: UserInput) -> pd.DataFrame:
    input_df = pd.DataFrame([{
                'property_type': user_input.property_type,
                'sector': user_input.sector.strip().lower(),
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
    return input_df


# home end point
@app.get('/')
def home():
    return {'message': 'Real estate price prediction model'}

# prediction end point
@app.post('/predict', response_model=PredictionResponse)
def make_prediction(user_input: UserInput):
    try:
        input_df = user_input_to_df(user_input)
        logging.info('Input data validated using pydantic and converted into dataframe object')

        prediction, price_unit = model.predict(input_df)
        predicted_price = round(prediction[0], 2)

        logging.info('Prediction pipeline successfully run')

        return PredictionResponse(
            predicted_price=predicted_price,
            price_unit=price_unit,
            message=f'The predicted price of the property is ₹ {predicted_price} {price_unit}'
        )
        
    except Exception as e:
        raise CustomeException(e, sys)
    
# insights end point 
@app.post('/explain', response_model=ExplainationResponse)
def explain(user_input: UserInput):
    try:
        input_df = user_input_to_df(user_input)
        logging.info('Input data validated using pydantic and converted into dataframe object')

        transformed_input = preprocessor.transform(input_df)
        prediction = rf_model.predict(transformed_input)

        # shap explainer
        explainer = shap.TreeExplainer(rf_model)
        shap_values = explainer.shap_values(transformed_input)

        feature_names = preprocessor.get_feature_names_out()

        contributions = dict(zip(feature_names, shap_values[0]))

        expected_value = explainer.expected_value

        return ExplainationResponse(
            predicted_price = prediction,
            feature_contributions = contributions,
            expected_value = expected_value
        )
    
    except Exception as e:
        raise CustomeException(e, sys)
    
   
# health check end point
@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION, 
        'model_loaded': model is not None
    }

