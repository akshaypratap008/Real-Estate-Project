import streamlit as st

st.title("Detailed Project Structure")
st.caption('This structure contains the major components of the project. Full structure can be found in GitHub repository at https://github.com/akshaypratap008/Real-Estate-Project')

st.markdown('''
```
real-estate-project/
├── main.py                          # Entry point for model training pipeline
├── setup.py                         # Package configuration
├── src/
│   ├── __init__.py
│   ├── exceptions.py                # Custom exception handling
│   ├── logger.py                    # Structured logging module
│   ├── utils.py                     # Shared utilities (save/load objects, model evaluation)
│   ├── components/
│   │   ├── __init__.py
│   │   ├── data_ingestion.py        # Load & split training data
│   │   ├── data_transformation.py   # Feature engineering & preprocessing pipeline
│   │   └── model_trainer.py         # Hyperparameter tuning & model training
│   ├── pipelines/
│   │   ├── __init__.py
│   │   ├── train_pipeline.py        # Orchestrates training workflow
│   │   └── predict_pipeline.py      # Inference pipeline for predictions
│   └── api/
│       ├── __init__.py
│       ├── app.py                   # FastAPI endpoints (/predict, /explain, /health)
│       └── schemas.py               # Pydantic validation models (UserInput, PredictionResponse)
├── streamlit-app/
│   ├── Home.py                      # Landing page
│   └── pages/
│       ├── 1_Prediction.py          # Price prediction UI
│       ├── 2_Analytics.py           # Data exploration & visualizations
│       ├── 3_Recommend_Societies.py # Society recommendations
│       └── 4_Insights.py            # Interactive feature analysis
├── artifacts/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── luxury_score.py          # Luxury metric calculation
│   │   ├── sector_mapping.py        # Sector encoding utilities
│   │   └── preprocessed-data/       # CSV snapshots for UI
│   ├── model.pkl                    # Trained RandomForest model
│   ├── preprocessor.pkl             # Preprocessing pipeline (ColumnTransformer)
│   ├── location_df.pkl              # Geographic distance matrix for recommendations
│   ├── cos_sim1/2/3.pkl             # Cosine similarity matrices
│   └── train.csv, test.csv          # Split datasets 
```
''')