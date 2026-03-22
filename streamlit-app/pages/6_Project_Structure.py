import streamlit as st

st.set_page_config(page_title="Project Structure", layout="wide")

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
│       ├── 4_Insights.py            # Interactive feature analysis
│       ├── 5_Project_Details.py     # In-depth information about technical architecture of the project
│       └── 6_Project_Structure      # Detailed project structure
├── artifacts/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── luxury_score.py          # Luxury metric calculation
│   │   ├── sector_mapping.py        # Sector encoding utilities
│   │   └── preprocessed-data/       # CSV snapshots containing csv files from major stages of the project
│   ├── model.pkl                    # Trained RandomForest model
│   ├── preprocessor.pkl             # Preprocessing pipeline (ColumnTransformer)
│   ├── location_df.pkl              # Geographic distance matrix for recommendations
│   ├── cos_sim1/2/3.pkl             # Cosine similarity matrices
│   └── train.csv, test.csv          # Split datasets for training and testing
```
''')