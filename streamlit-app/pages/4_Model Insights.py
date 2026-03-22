import pandas as pd
import numpy as np
import shap
import streamlit as st
import requests
import sys
import plotly.express as px
import plotly.graph_objects as go

from src.api.schemas import UserInput, ExplainationResponse
from src.exceptions import CustomeException
import streamlit.components.v1 as components


# data
df = pd.read_csv('artifacts/data/preprocessed-data/gurgaon_properties_post_feature_selection.csv')
EXPLAIN_API_URL = "https://real-estate-model-api-1097778515095.europe-west1.run.app/explain"

st.set_page_config(page_title="Insights Playground", layout="wide")

st.header('Insights Playground')
st.caption('*Experiment with different property configurations and understand how each feature influences the predicted price.*')

st.divider()


with st.sidebar:
    st.write('Select Features')
    property_type = st.radio(label= 'Property Type', options = ['Flat', 'House'])
    sector = st.selectbox(label = 'Sector', options = [i.upper() for i in df['sector'].unique()])
    bedroom = st.slider(label = 'Bedrooms', min_value=1, max_value = 10)
    bathroom = st.slider(label = 'Bathrooms', min_value= 1, max_value = 10)
    balcony = st.radio(label = 'Balcony', options = ['1', '2', '3+'])
    agePossession = st.selectbox(label = 'Age / Possession', options = [i.upper() for i in df['agePossession'].unique()])
    built_up_area = st.slider(label = 'Built-up Area (Sqft)', min_value = 500, max_value = 20000)
    servant_room = st.toggle(label = 'Servant Room')
    store_room = st.toggle(label = 'Store Room')
    furnishing_type = st.radio(label = 'Furnishing Type', options = ['Unfurnished', 'Semifurnished', 'Furnished'])
    luxury_category = st.radio(label = 'Luxury Category', options = ['Budget', 'Luxury'])
    floor_category = st.radio(label = 'Floor Category', options = ['Low-rise', 'Medium-rise', 'High-rise'])

    # data validation using pydantic model 
input_data: UserInput = {
    'property_type': property_type.lower(),
    'sector': sector,
    'bedroom' : bedroom,
    'bathroom' : bathroom,
    'balcony' : balcony,
    'agePossession' : agePossession,
    'built_up_area' : built_up_area,
    'servant_room' : servant_room,
    'store_room' : store_room,
    'furnishing_type' : furnishing_type.lower(), 
    'luxury_category' : luxury_category.lower(),
    'floor_category' : floor_category.lower()
}

input_data = UserInput(**input_data)
try:
    with st.spinner('Loading...'):
        response = requests.post(url = EXPLAIN_API_URL, json = input_data.model_dump())
        if response.status_code == 200:
            json_result = response.json()
            # json_result = ExplainationResponse(**json_result)

            expected_value = round(np.expm1(json_result['expected_value']), 2)
            pridicted_price = round(np.expm1(json_result['predicted_price']), 2)
            shap_value_dict = json_result['feature_contributions']
            shap_values_df = pd.DataFrame(list(shap_value_dict.items()), columns=['Feature', 'Value'])
            shap_values_df['Feature'] = ['Built-up Area', 'Age / Possession', 'Furnishing Type', 'Bedrooms', 'Bathrooms', 'Servant Room', 'Store Room', 'Property Type: House', 'Balcony: 1', 'Balcony: 2', 'Balcony: 3', 'Balcony: 3+', 'Luxury Category: Luxury', 'Luxury Category: Semi-luxury', 'Floor Category: Low-rise', 'Floor Category: Medium-rise', 'Sector']

            shap_values_df = shap_values_df.sort_values('Value', ascending = False)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader('Model Summary')
                colx, coly = st.columns(2)
                with colx:
                    st.metric('Predicted Price', f'₹ {pridicted_price} Cr', border = True, height = 'content')
                with coly:
                    st.metric("Model's baseline Pirce", f'₹ {expected_value} Cr', border = True, height = 'content')

                
                delta_value = round(pridicted_price - expected_value, 2)
                st.metric(
                    label='Difference from Baseline Price',
                    value=f'₹ {delta_value} Cr',
                    delta=delta_value,          
                    border=True,
                    height='content',
                    delta_color="normal"
                    )

                st.divider()

                col3, col4 = st.columns(2)
                top_pos = shap_values_df.head(3)
                top_neg = shap_values_df.tail(3).sort_values('Value')
                with col3:
                    st.markdown('#### Features **increasing** the price')
                    for i in top_pos['Feature']:
                        st.markdown(f'- :green[{i}]')
                with col4:
                    st.markdown('#### Features **decreasing** the price')
                    for i in top_neg['Feature']:
                        st.markdown(f'- :red[{i}]')
                

            with col2:
                st.subheader("Feature Impact")
                
                fig = px.bar(shap_values_df.sort_values('Value', ascending = True), x = 'Value', y = 'Feature', orientation='h', color = 'Value', color_continuous_scale='RdBu')
                st.plotly_chart(fig, use_container_width=True, key = '', height = 570)

            st.divider()

            # shap waterfall chart
            left, center, right = st.columns([0.5, 3, 0.5])
            with center:
                st.subheader("SHAP Waterfall Chart", text_alignment='center')
                fig = go.Figure(go.Waterfall(name = "SHAP", orientation = 'v', x = shap_values_df['Feature'], y = shap_values_df['Value']))
                st.plotly_chart(fig, use_container_width=True)

            
        else:
            st.error(f"API error: {response.status_code} - {response.text}")

except Exception as e:
    raise CustomeException(e, sys)
    

