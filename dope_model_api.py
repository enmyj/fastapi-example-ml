from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from joblib import load
import pandas as pd
import json

app = FastAPI()

# load pickled files
rfc = load('iris_rfc.joblib')


# Define individual row classes
class Iris(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


# define data class
class Irises(BaseModel):
    data: List[Iris]


@app.post('/predict/', status_code=200)
async def model_predict(irises: Irises):

    # load row(s) passed into df
    row = pd.DataFrame(irises.dict()['data'])

    # make prediction(s)
    return json.dumps(list(rfc.predict(row)))
