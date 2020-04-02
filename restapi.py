# %% Imports
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from sqlalchemy import create_engine


# %% Globals
eng = create_engine('sqlite:///./mtcars.sqlite')
df = pd.read_sql('mtcars', eng)
app = FastAPI()


# define mtcars fields and types
class MtCars(BaseModel):
    mpg: float
    cyl: int
    disp: float
    hp: int
    drat: float
    wt: float
    qsec: float
    vs: int
    am: int
    gear: int
    carb: int


# %% Get Data from DB
@app.get('/v1/', status_code=200)
async def mtcars_get(
    cyl: int,
    mpg_min: float,
    am: int = 0
):
    """ Return mtcars filtered down to only selected rows

    Client will use query parameters to select rows

    Args:
        cyl (int): number of cylinders
        mpg_min (float): minimum mpg
        am (int): 0 = automatic, 1 = manual

    Returns:
        pandas dataframe converted to json
    """
    # row filters
    conds = (
        (df['cyl'] == cyl) &
        (df['mpg'] >= mpg_min) &
        (df['am'] == am)
    )

    # new dataframe with filters applied
    out = df.loc[conds, :]

    # raise error if no rows returned
    if out.empty:
        raise HTTPException(400, "No Rows Returned")

    return out.to_json()


# %% Send data to DB
@app.post('/v1/', status_code=200)
async def mtcars_post(mtcar: MtCars):
    """ Append rows to mtcars.sqlite database:

    mpg: Miles/(US) gallon \n
    cyl: Number of cylinders \n
    disp: Displacement (cu.in.) \n
    hp: Gross horsepower \n
    drat: Rear axle ratio \n
    wt: Weight (1000 lbs) \n
    qsec: 1/4 mile time \n
    vs: V/S \n
    am: Transmission (0 = automatic, 1 = manual) \n
    gear: Number of forward gears \n
    carb: Number of carburetors
    """

    # convert mtcar (1-row dict) to dataframe
    row = pd.DataFrame([mtcar.dict()])  # haha pandas is so weird

    # append to sqlite database
    row.to_sql(
        name='mtcars',
        con=eng,
        if_exists='append',
        index=False
    )

    return 'success'
