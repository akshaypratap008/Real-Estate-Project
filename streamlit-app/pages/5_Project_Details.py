import streamlit as st

st.set_page_config(page_title="Project Details", layout="wide")

st.title('🛠️ Technical Architecture & Implementation')
st.link_button(label = 'Visit Repository on GitHub', url= 'https://github.com/akshaypratap008/Real-Estate-Project')

st.markdown('''
This project demonstrates production-grade data science engineering:

- End-to-end ML pipeline from raw data → persisted model → API → Docker Containerization -> interactive UI
- Thoughtful feature engineering with domain-specific transformations (log scaling for area, target encoding for location)
- Explainable AI through SHAP integration
- Scalable architecture with cloud deployment
- Professional Python practices: modular code, error handling, logging, type safety
- Full-stack capability: backend ML engineering + frontend UX''', text_alignment='justify')

st.markdown('''
            #### 1. Project Structure & Design Patterns
            ```
            real-estate-project/
            ├── src/
            │   ├── components/          # Data pipeline components
            │   ├── pipelines/           # Training & prediction workflows
            │   ├── api/                 # FastAPI backend
            │   ├── exceptions.py        # Custom error handling
            │   ├── logger.py            # Structured logging
            │   └── utils.py             # Shared utilities
            ├── streamlit-app/           # Frontend UI
            ├── artifacts/               # Persisted models & data
            └── main.py                  # Entry point
            ```
            ''')
if st.button('Detailed Project Structure'):
    st.switch_page('pages/6_Project_Structure.py')

st.markdown('''
            #### 2. Data Pipeline (ETL)

            **Data Ingestion:**
            - Source: Preprocessed Gurgaon real estate properties dataset scrapped from 99acres.com
            - Raw data persisted to data.csv
            - Stratified train-test split (80/20) with random_state=42 for reproducibility

            **Feature Engineering & Transformation:**
            ```
            Numerical Features → Log transformation (log1p) + StandardScaler
            - built_up_area (highly skewed)
            - bedRoom, bathroom, servant room, store room

            Categorical Features:
            - One-Hot Encoding: property_type, balcony, luxury_category, floor_category
            - Ordinal Encoding: agePossession, furnishing_type
            - Target Encoding: sector (leverages price correlation)

            Target Transformation: 
            - Price → log1p(price) to normalize exponential distribution
            ```

            **Preprocessing Pipeline:**
            Built with ```sklearn.compose.ColumnTransformer``` for reproducibility
            Fitted on training set, applied identically to test & inference data
            Persisted as ```preprocessor.pkl``` for inference consistency

            ''')

st.markdown('''
            #### 3. ML Model Training
            **Algorithm Selection:**
            - RandomForestRegressor - chosen for:
                -   Strong MAE and R2 score
                -   Strong handling of non-linear relationships in real estate pricing
                -   Feature importance interpretation
                -   SHAP explainability support (TreeExplainer)
                -   Robustness to outliers
                -   Hyperparameter Optimization:
            
            **Hyperparameter Optimization:**
            - RandomizedSearchCV with 10-fold cross-validation (KFold shuffle=True)
            - Grid parameters:
                -   n_estimators: [250, 300, 350, 400]
                -   max_depth: [25, 30, 35]
                -   min_samples_split: [2, 3, 4]
                -   min_samples_leaf: [1, 2]
                -   max_features: [None, 'sqrt']
                -   30 iterations across parameter space for optimal performance
            
            **Model Evaluation:**
            - Primary Metric: MAE (Mean Absolute Error) on train & test sets
            - Secondary Metric: R² score via cross-validation
            - Logging of all metrics for model tracking
            
            **Artifact Persistence:**

            - Trained model → ```model.pkl``` (dill serialization for compatibility)
            - Preprocessor → ```preprocessor.pkl```
            ''')

st.markdown('''
            #### 4. Backend API (FastAPI)
            **Endpoints:**
            | Endpoint        | Method | Purpose                                 |
            |-----------------|--------|-----------------------------------------|
            | ```/```         | GET    | API description                         |
            | ```/predict```  | POST   | Single property price prediction        |
            | ```/explain```  | POST   | SHAP-based feature contribution analysis|
            | ```/health```   | GET    | API, model status & version control     |

            **Input Validation:**
            - Pydantic ```UserInput``` schema with strict type hints & descriptive error messages
            - Literal types enforce category constraints (e.g., property_type: 'flat' | 'house')
            
            **Prediction Response:**
            - ```PredictionResponse```: predicted_price + price_unit (auto-converts to Lakhs/Crores)
            - ```ExplainationResponse```: prediction + SHAP feature contributions + expected value
            
            **SHAP Integration for Model Interpretability:**

            - ```TreeExplainer``` initialized on RandomForest model
            - Per-prediction feature attribution scores
            - Enables users to understand individual prediction drivers
            ''')

st.markdown('''
            #### 5. Frontend (Streamlit)
            **Multi-page App Architecture:**
            - ```Home.py``` - Landing page with project overview
            - ```1_Price Prediction.py``` - Form-based interface calling /predict & /explain endpoints
            - ```2_Market Analytics.py``` - Data exploration (maps, wordclouds, scatter plots, pie charts)
            - ```3_Society Recommendations.py``` - Cosine similarity-based society recommendations using precomputed similarity matrices
            - ```4_Model Insights.py``` - Interactive feature slider for real-time SHAP-based sensitivity analysis
            - ```5_Project_Details``` - Technical Architecture and Implementation of the project
            - ```6_Project_Structure``` - Detailed Project Structure
            
            **UI/UX Details:**
            - Responsive 3-column layouts for dense form inputs
            - Real-time data loading from preprocessed CSVs
            - Plotly for interactive visualizations (scatter maps, bar charts)
            - Session state management for stateful recommendations
            - Spinner feedback during API calls
            - Error handling with custom exceptions

            **Recommendation Engine:**
            - Precomputed cosine similarity matrices (```cos_sim1.pkl```, ```cos_sim2.pkl```, ```cos_sim3.pkl```)
            - Weighted ensemble: ```0.2*sim1 + 0.8*sim2 + 0.1*sim3```
            - Radius-based geospatial filtering using precomputed distance matrices
            
            ''')

st.markdown('''
            #### 6. Advanced Features
            **Reproducibility:**
            - Fixed random seeds (random_state=42) across train/test splits, CV, hyperparameter search
            - Deterministic preprocessing pipeline
            - Versioned model artifacts
            
            **Scalability Considerations:**

            - ***Backend API:*** FastAPI deployed on Google Cloud Run (URL: https://real-estate-model-api-1097778515095.europe-west1.run.app
            - ***Frontend UI***: Streamlit app also deployed on Google Cloud Run (URL: https://real-estate-ui-1097778515095.europe-west1.run.app)
            - Async request handling for concurrent predictions
            - ***Containerization***: Both services deployed using Docker containers, with images available on Docker Hub for easy replication, version control, and deployment across environments. Link to Docker hub - https://hub.docker.com/u/akshay0008
            
            **Logging & Monitoring:**
            - Structured logging with ```src.logger``` (custom logger module)
            - API request/response logging
            - Exception tracking with custom ```CustomeException``` wrapper
            
            **Error Handling:**
            - Custom exception hierarchy (CustomeException) with traceback preservation
            - Try-catch blocks in all critical paths
            - Meaningful error messages propagated to frontend
            ''')


st.markdown('''
            #### 7. CI/CD Pipeline (GitHub Actions)
            - Fully automated build + deploy pipeline using GitHub Actions
            - Workflow triggers:
                - `push` on `main` 
            - Stages:
                - `build` (package + Docker image)
                - `deploy` (Cloud Run deployment for API and Streamlit UI)
            - Docker image publishing to Docker Hub
            
''')
st.markdown('''
            #### 8. Sector Mapping & Luxury Scoring
            **Special Data Features:**
            - ```sector_mapping.py``` — Likely sector encoding/mapping utilities build using Google Maps Geocoding API
            - ```luxury_score.py``` — Derived luxury metric for property classification. Classification done using KMean clustering algorithm. 
            - Latitude/Longitude precomputation for geospatial analysis (gurgaon_properties_with_lat_long.csv)''')

st.caption('The description of the project is gerenated using copilot', text_alignment='right')