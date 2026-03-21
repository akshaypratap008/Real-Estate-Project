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
COPY artifacts ./artifacts

# copy src folder
COPY src ./src

# expose the ports
EXPOSE 8080

# comand to start streamlit
CMD ["streamlit", "run", "streamlit-app/Home.py", "--server.port=8080", "--server.address=0.0.0.0"]
