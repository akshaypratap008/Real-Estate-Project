# base image
FROM python:3.11-slim

# set work dir
WORKDIR /app

#copy requirements and install dependencies
COPY requirements/api.txt .
RUN pip install --no-cache-dir -r api.txt

# copy api code
COPY src/api /app/src/api
# - copy src/api and add to /app/src/api inside container

#copy pipeline
COPY src/pipelines /app/src/pipelines      
# - docker file will be run from root directory. Copy src/pipeline and add into /app/src/pipelines inside the container

#copy model artifacts
COPY artifacts /app/artifacts

#copy utils, exception,logger file
COPY src/utils.py /app/src/utils.py
COPY src/exceptions.py /app/src/exceptions.py
COPY src/logger.py /app/src/logger.py

# expose the application port
EXPOSE 8000

# comand to start Fast API
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]