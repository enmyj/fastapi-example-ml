# %%
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()


# %%
@app.post('/predict/', status_code=200)
def model_predict():
    # TODO: load pickled model (and any transformers)
    # TODO: intake and process data passed by user
    # TODO: make a model prediction and return results!
    # TODO: Extra Credit: How would you write this to intake mulitiple rows of data and return multiple predictions?
    pass
