import pandas as pd
import numpy as np
import streamlit as st

st.subheader("Baseline Property")
st.caption("This is the reference property used for comparison.")

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

col1, col2 = st.columns(2)
with col1:
    st.write("Bedrooms:", baseline['bedRoom'])
    st.write("Bathrooms:", baseline['bathroom'])
    st.write("Area:", baseline['built_up_area'])
with col2:
    st.write("Property Type:", baseline['property_type'])
    st.write("Sector:", baseline['sector'])
    st.write("Furnishing:", baseline['furnishing_type'])
