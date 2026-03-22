# Real Estate Project

## Overview

A full-stack real estate price prediction platform for Gurgaon, India.

- End-to-end ML pipeline (data ingestion, transformation, model training).
- FastAPI backend with model prediction and SHAP-based explainability.
- Streamlit interactive dashboard for prediction, analytics, and recommendations.
- App delivers price estimates in crores/lakhs based on user inputs.

## Repository Structure

- `main.py`: Basic FastAPI skeleton for health check and simple endpoints.
- `setup.py`: Package setup and dependency loader.
- `requirements.txt`: Python dependencies.
- `src/`
  - `api/`: FastAPI routes and Pydantic schemas.
  - `components/`: Core pipeline modules:
    - `data_ingestion.py`: loads preprocessed CSV, splits train/test.
    - `data_transformation.py`: encoding, scaling, and preprocessing pipeline.
    - `model_trainer.py`: hyperparameter tuning (RandomForest via RandomizedSearchCV) and model persistence.
  - `pipelines/`:
    - `predict_pipeline.py`: loading model/preprocessor, predicting and unit conversion.
    - `train_pipeline.py`: currently empty, training flow is in `components` modules.
  - `utils.py`: object serialization, model evaluation helper.
  - `logger.py`: logging configuration.
  - `exceptions.py`: custom exception wrapper.
- `artifacts/data/`: preprocessed dataset and mapping utilities.
- `streamlit-app/`: multi-page Streamlit UI.

## Features

1. Data Ingestion
   - Reads `artifacts/data/preprocessed-data/gurgaon_properties_post_feature_selection.csv`.
   - Saves raw, train, test datasets in `artifacts/`.

2. Preprocessing Pipeline
   - Log transform + StandardScaler for `built_up_area`.
   - Ordinal encoding for `agePossession`, `furnishing_type`.
   - One-hot for `property_type`, `balcony`, `luxury_category`, `floor_category`.
   - Target encoder for `sector`.

3. Model Training
   - RandomForest regression with hyperparameter search.
   - Saves best model to `artifacts/model.pkl`.

4. REST API
   - `GET /`: project info.
   - `GET /health`: status and model version.
   - `POST /predict`: price prediction.
   - `POST /explain`: SHAP feature contributions.

5. Streamlit App
   - Price prediction page (with API integration and SHAP explanation).
   - Market analytics, residence recommendations, model insights, docs.

## Setup (local)

1. Python 3.10+ recommended.
2. Create virtual env:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

3. (Optional) Install project in editable mode:

```bash
pip install -e .
```

## Run FastAPI Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- API docs: `http://127.0.0.1:8000/docs`

## Run Streamlit Dashboard

```bash
streamlit run streamlit-app/Home.py
```

## Model Training Workflow

1. Ensure dataset exists at `artifacts/data/preprocessed-data/gurgaon_properties_post_feature_selection.csv`.
2. Execute training script via module entrypoint:

```bash
python -c "from src.components.data_ingestion import DataIngestion; import pandas as pd; ..."
```

or run manually from `src/components/data_ingestion.py` section:

```bash
python src/components/data_ingestion.py
```

This triggers:
- Data ingestion (train/test split)
- Preprocessing saved as `artifacts/preprocessor.pkl`
- Model training saved as `artifacts/model.pkl`

## API Request Examples

### Predict

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "property_type": "flat",
    "sector": "sector 14",
    "bedroom": 3,
    "bathroom": 2,
    "balcony": "2",
    "agePossession": "new",
    "built_up_area": 1500,
    "servant_room": false,
    "store_room": false,
    "furnishing_type": "furnished",
    "luxury_category": "budget",
    "floor_category": "medium-rise"
  }'
```

### Explain

```bash
curl -X POST http://127.0.0.1:8000/explain -H "Content-Type: application/json" -d @input.json
```

## Notes

- `streamlit-app/pages/1_Price Prediction.py` currently uses hard-coded URLs to deployed API endpoints.
- self-hosting requires updating `PREDICTION_API_URL` / `EXPLAINATION_API_URL` to local `http://127.0.0.1:8000`.


