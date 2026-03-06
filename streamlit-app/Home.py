import streamlit as st

st.set_page_config(page_title="Real Estate Price Predictor", layout="wide")

st.title("🏡 Real Estate Price Prediction Project")
st.subheader("End‑to‑end ML system for property price estimation")

st.markdown("""
### Project Overview
This application predicts real‑estate prices based on property features such as:
- Property type  
- Sector  
- Bedrooms, bathrooms  
- Built‑up area  
- Furnishing, luxury category  
- Floor category  
- And more...

Use the sidebar to navigate:
- **Prediction** → Get price estimate  
- **Analytics** → Explore data insights  
""")
