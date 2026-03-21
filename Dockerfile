# base image
FROM python:3.11-slim

# working dir inside the container
WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# copy requirements and install dependencies
COPY requirements/streamlit.txt ./requirements/streamlit.txt
RUN pip install --no-cache-dir -r ./requirements/streamlit.txt

# copy streamlit code files 
COPY streamlit-app/Home.py ./streamlit-app/Home.py
COPY streamlit-app/pages ./streamlit-app/pages

# copy artifacts
COPY artifacts/data/preprocessed-data/gurgaon_properties_with_lat_long.csv ./artifacts/data/preprocessed-data/gurgaon_properties_with_lat_long.csv
COPY artifacts/data/preprocessed-data/gurgaon_properties_post_feature_selection.csv ./artifacts/data/preprocessed-data/gurgaon_properties_post_feature_selection.csv
COPY artifacts/data/preprocessed-data/gurgaon_properties_cleaned_v1.csv ./artifacts/data/preprocessed-data/gurgaon_properties_cleaned_v1.csv

# copy pickle files
COPY artifacts/location_df.pkl ./artifacts/location_df.pkl
COPY artifacts/cos_sim1.pkl ./artifacts/cos_sim1.pkl
COPY artifacts/cos_sim2.pkl ./artifacts/cos_sim2.pkl
COPY artifacts/cos_sim3.pkl ./artifacts/cos_sim3.pkl

# copy other files
COPY src/api/schemas.py ./src/api/schemas.py
COPY src/exceptions.py ./src/exceptions.py
COPY src/logger.py ./src/logger.py

# expose the ports
EXPOSE 8080

# comand to start streamlit
CMD ["streamlit", "run", "streamlit-app/Home.py", "--server.port=8080", "--server.address=0.0.0.0"]
