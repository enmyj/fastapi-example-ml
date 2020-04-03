from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
import pandas as pd

app = FastAPI()


class Iris(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@app.post('/predict/', status_code=200)
async def model_predict(iris: Iris):
    # le = load('iris_le.joblib')
    # pred = rfc.predict(row)
    # return le.inverse_transform(pred)[0]

    # load row passed into df
    row = pd.DataFrame([iris.dict()])

    # load pickled files
    rfc = load('iris_rfc.joblib')

    # make prediction
    return rfc.predict(row)[0]
