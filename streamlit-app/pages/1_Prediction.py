import streamlit as st
import numpy as np
import pandas as pd
import requests
from src.api.schemas import UserInput
from src.exceptions import CustomeException
import sys

#load dataframe to add options in the form 
df = pd.read_csv(r'C:\Users\apaks\Desktop\Real Estate Project\artifacts\data\preprocessed-data\gurgaon_properties_post_feature_selection.csv')

sectors = sorted(df['sector'].unique())
age_possesion = df['agePossession'].unique()

# api url
API_URL = "http://127.0.0.1:8000/predict"

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
input_data = {
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

# ---- prediction ----
if st.button("Predict Price"):
    try:
        response = requests.post(url=API_URL, json=input_data)
        if response.status_code == 200:
            result = response.json()
            st.success(result)
        else:
            st.error(f"API error: {response.status_code} - {response.text}")
    except Exception as e:
        raise CustomeException(e, sys)

    
