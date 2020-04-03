from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from joblib import load
import pandas as pd
import json

app = FastAPI()


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
    # le = load('iris_le.joblib')
    # pred = rfc.predict(row)
    # return le.inverse_transform(pred)[0]

    # load row(s) passed into df
    row = pd.DataFrame(irises.dict()['data'])

    # load pickled files
    rfc = load('iris_rfc.joblib')

    # make prediction(s)
    return json.dumps(list(rfc.predict(row)))
