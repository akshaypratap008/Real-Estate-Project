from fastapi import FastAPI

app = FastAPI()

@app.get('/')       #route for the end point. get request
def hello():
    return {'message': 'helldfo world'}

@app.get('/about')
def my_name():
    return {'message': 'Akshay and Preet'}