import streamlit as st
import numpy as np
import pandas as pd
import requests
from src.api.schemas import UserInput, PredictionResponse
from src.exceptions import CustomeException
import sys

#load dataframe to add options in the form 
df = pd.read_csv('artifacts\data\preprocessed-data\gurgaon_properties_post_feature_selection.csv')

sectors = sorted(df['sector'].unique())
age_possesion = df['agePossession'].unique()

# api url
PREDICTION_API_URL = "http://127.0.0.1:8000/predict"

st.title("🏠 Price Prediction")

# ---- user input ----
property_type = st.selectbox('Property Type', ['flat', 'house'])
sector = st.selectbox('Sector', sectors)
bedroom = st.number_input('Bedrooms', min_value=1, max_value=20, step=1)
bathroom = st.number_input('Bathrooms', min_value=1, max_value=10, step=1)
balcony = st.selectbox('Balcony', ['1', '2', '3+'])
agePossession = st.selectbox('Age / Possession', age_possesion)
built_up_area = st.number_input('Built-up Area (sq ft)', min_value=100, max_value=20000)
servant_room = st.selectbox('Servant Room', ['Yes', 'No'])
store_room = st.selectbox('Store Room', ['Yes', 'No'])
furnishing_type = st.selectbox('Furnishing Type', ['unfurnished', 'semifurnished', 'furnished'])
luxury_category = st.selectbox('Luxury Category', ['budget', 'luxury'])
floor_category = st.selectbox('Floor Category', ['low-rise', 'medium-rise', 'high-rise'])

# convert user input into pydantic object
input_data: UserInput = {
    'property_type': property_type,
    'sector': sector,
    'bedroom' : bedroom,
    'bathroom' : bathroom,
    'balcony' : balcony,
    'agePossession' : agePossession,
    'built_up_area' : built_up_area,
    'servant_room' : servant_room,
    'store_room' : store_room,
    'furnishing_type' : furnishing_type, 
    'luxury_category' : luxury_category,
    'floor_category' : floor_category
}

input_data = UserInput(**input_data)        # input validating using the pydantic model

# ---- prediction ----
if st.button("Predict Price"):
    try:
        response = requests.post(url=PREDICTION_API_URL, json=input_data.model_dump())      #model dump converts the pydantic model into json
        if response.status_code == 200:
            json_result = response.json()
            json_result = PredictionResponse(**json_result)   # response validation and convert into pydantic model
            json_result = json_result.model_dump()      # pydantic model converted again into dict to show results
            result = json_result['message']
            st.success(result)
        else:
            st.error(f"API error: {response.status_code} - {response.text}")
    except Exception as e:
        raise CustomeException(e, sys)

    
