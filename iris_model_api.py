import json
from typing import List

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
import pandas as pd

app = FastAPI()
rfc = load('iris_rfc.joblib')  # load pickled model


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

    # load row(s) passed into a df
    row = pd.DataFrame(irises.dict()['data'])

    # make prediction(s) and output as json
    return json.dumps(list(rfc.predict(row)))


if __name__ == "__main__":
    # For debugging
    # Use editor to place breakpoints then hit API
    # using Postman, FastAPI docs, requests, curl, etc.
    uvicorn.run(app, host="0.0.0.0", port=8000)
