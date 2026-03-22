import streamlit as st
import numpy as np
import pandas as pd
import requests
from src.api.schemas import UserInput, PredictionResponse, ExplainationResponse
from src.exceptions import CustomeException
import sys
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Price Prediction", layout="wide")
#load dataframe to add options in the form 
df = pd.read_csv('artifacts/data/preprocessed-data/gurgaon_properties_post_feature_selection.csv')

sectors = sorted(df['sector'].unique())
age_possesion = df['agePossession'].unique()

# api url
PREDICTION_API_URL = "https://real-estate-model-api-1097778515095.europe-west1.run.app/predict"
EXPLAINATION_API_URL = "https://real-estate-model-api-1097778515095.europe-west1.run.app/explain"




st.title("🏠 Price Prediction")
st.caption("*Input property details and get predictions with explanation*")
st.divider()

# ---- user input ----
st.subheader('Property Details')
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        property_type = st.selectbox('Property Type', ['Flat', 'House'])
        sector = st.selectbox('Sector', sectors)
        built_up_area = st.number_input('Built-up Area (sq ft)', min_value=100, max_value=20000, step = 50)
        agePossession = st.selectbox('Age / Possession', age_possesion)

    with col2:
        bedroom = st.number_input('Bedrooms', min_value=1, max_value=20, step=1)
        bathroom = st.number_input('Bathrooms', min_value=1, max_value=10, step=1)
        servant_room = st.selectbox('Servant Room', ['Yes', 'No'])
        store_room = st.selectbox('Store Room', ['Yes', 'No'])

    with col3:
        balcony = st.selectbox('Balcony', ['1', '2', '3+'])
        furnishing_type = st.selectbox('Furnishing Type', ['Unfurnished', 'Semifurnished', 'Furnished'])
        luxury_category = st.selectbox('Luxury Category', ['Budget', 'Luxury'])
        floor_category = st.selectbox('Floor Category', ['Low-rise', 'Medium-rise', 'High-rise'])

# convert user input into pydantic object
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

input_data = UserInput(**input_data)        # input validating using the pydantic model

# ---- prediction ----
col1, col2, col3 = st.columns([1,2,1])

if st.button("Predict Price"):
    try:
        with st.spinner("Predicting price..."):
            response = requests.post(url=PREDICTION_API_URL, json=input_data.model_dump())      #model dump converts the pydantic model into json
            if response.status_code == 200:
                json_result = response.json()
                json_result = PredictionResponse(**json_result)   # response validation and convert into pydantic model
                json_result = json_result.model_dump()      # pydantic model converted again into dict to show results
                result = json_result['message']

                with st.container():
                    st.success(result)
            else:
                st.error(f"API error: {response.status_code} - {response.text}")
    except Exception as e:
        raise CustomeException(e, sys)


#---------------------------------Explaination MODULE----------------------------------
    try:
        response = requests.post(url=EXPLAINATION_API_URL, json=input_data.model_dump())      #model dump converts the pydantic model into json
        if response.status_code == 200:
            json_result = response.json()
            json_result = ExplainationResponse(**json_result)   # response validation and convert into pydantic model
            json_result = json_result.model_dump()      # pydantic model converted again into dict to show results

            expected_value = round(np.expm1(json_result['expected_value']), 2)
            pridicted_price = round(np.expm1(json_result['predicted_price']), 2)
            shap_value_dict = json_result['feature_contributions']
            shap_values_df = pd.DataFrame(list(shap_value_dict.items()), columns=['Feature', 'Value'])
            shap_values_df['Feature'] = ['Built-up Area', 'Age / Possession', 'Furnishing Type', 'Bedrooms', 'Bathrooms', 'Servant Room', 'Store Room', 'Property Type: House', 'Balcony: 1', 'Balcony: 2', 'Balcony: 3', 'Balcony: 3+', 'Luxury Category: Luxury', 'Luxury Category: Semi-luxury', 'Floor Category: Low-rise', 'Floor Category: Medium-rise', 'Sector']

            shap_values_df = shap_values_df.sort_values('Value', ascending = False)
            
            st.divider()

            st.subheader('Prediction Summary')
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric('Predicted Price', f'₹ {pridicted_price} Cr', border = True, height='stretch')

            with col2:
                st.metric("Model's baseline Pirce", f'₹ {expected_value} Cr', border = True, height='stretch')

            with col3:
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

            st.subheader('Top Factors Affecting Price')
            top_pos = shap_values_df.head(5)
            top_neg = shap_values_df.tail(5).sort_values('Value')

            col1, col2 = st.columns(2)
            with col1:
                st.markdown('📈 Increasing Price')
                for _, row in top_pos.iterrows():
                    st.badge(label = f"**{row['Feature']}** → +₹ {round(row['Value'], 2)} Cr", color="blue")
            
            with col2:
                st.markdown('📉 Decreasing Price')
                for _, row in top_neg.iterrows():
                    st.badge(label = f"**{row['Feature']}** → ₹ {round(row['Value'], 4)} Cr", color="red")
            st.caption("The values above are SHAP values for different features")

            col1, col2 = st.columns(2)
            with col1:
                st.divider()
                # bar chart feature Impact
                st.subheader("Feature Impact")
                fig = px.bar(shap_values_df.sort_values('Value', ascending = True), x = 'Value', y = 'Feature', orientation='h', color = 'Value', color_continuous_scale='RdBu')
                left, center, right = st.columns([1,3,1])
                with center:
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.divider()
                # shap waterfall chart
                st.subheader("SHAP Waterfall Chart")
                fig = go.Figure(go.Waterfall(name = "SHAP", orientation = 'v', x = shap_values_df['Feature'], y = shap_values_df['Value']))
                left, center, right = st.columns([1,3,1])
                with center:
                    st.plotly_chart(fig, use_container_width=True)
            
            st.divider()

            # Natural language explaination
            st.subheader("Explanation")

            st.markdown(
            f"""
            The model's baseline predicted price is **₹ {expected_value} Cr**.

            For this property:

            - The strongest :green[POSITIVE] contributor is **{top_pos.iloc[0]['Feature']}**,  
            adding :green[**₹ {round(top_pos.iloc[0]['Value'], 3)} Cr**].

            - The strongest :red[NEGATIVE] contributor is **{top_neg.iloc[0]['Feature']}**,  
            reducing the price by :red[**₹ {round(top_neg.iloc[0]['Value'], 3)} Cr**].

            Together, these factors shape the final predicted price of **₹ {pridicted_price} Cr**.
            """
            )


        else:
            st.error(f"API error: {response.status_code} - {response.text}")
    except Exception as e:
        raise CustomeException(e, sys)