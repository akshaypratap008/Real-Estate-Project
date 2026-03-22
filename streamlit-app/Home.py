import streamlit as st

st.set_page_config(page_title="Real Estate Price Predictor", layout="wide")

st.title("🏡 Real Estate Price Prediction Project")
st.subheader("An end‑to‑end ML system for property price estimation in Gurgaon.")

st.markdown("""
            This application predicts real estate prices based on comprehensive property features, helping users and investors make data-driven decisions about property valuations.
            ### Key Features & What Users Can Do:

            #### 1. 🏠 Price Prediction Page
            - Input property details (property type, sector, bedrooms, bathrooms, built-up area, etc.)
            - Instant price prediction powered by machine learning
            - Get predicted price in Lakhs or Crores depending on value
            - Understand price drivers through SHAP-based feature explanations showing which attributes increase or decrease the predicted price

            #### 2. 📊 Market Analytics
            - Geospatial Analysis: Interactive map showing average price-per-sqft across Gurgaon sectors with geographic visualization
            - Features Wordcloud: Visualize the most frequently mentioned amenities and selling points across listings
            - Area vs Price Scatter Plot: Explore how property prices scale with built-up area, color-coded by bedroom count
            - Property Mix Insights: Pie charts showing bedroom distribution both overall and sector-wise
            - Filter by property type (Flat/House) for custom analysis

            #### 3. 🗺️ Society Recommendations
            - Search for societies within a specific landmark radius (1-60 km)  
            - Get AI-powered recommendations for similar properties based on:
                -   Location similarity
                -   Price characteristics
                -   Property features
            - View similarity scores for each recommended society

            #### 4. 🔍 Model Insights
            - Real-time interactive feature slider controls (property type, bedrooms, bathrooms, location, luxury level, etc.)
            - Instantly see how parameter changes impact predicted price
            - Side-by-side comparison of:
                -   Predicted price vs model baseline
                -   Top 3 features increasing the price
                -   Top 3 features decreasing the price
            - SHAP-powered interpretability to understand model reasoning
            """)

if st.button(label = 'View Technical Implementation'):
    st.switch_page("pages/5_Project_Details.py")




