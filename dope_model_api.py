# %%
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import pickle

app = FastAPI()


# %%
@app.post('/predict/', status_code=200)
def model_predict():
    # TODO: load pickled model
    # TODO: parse data passed by user
    # TODO: make a model prediction and return results!
    pass
