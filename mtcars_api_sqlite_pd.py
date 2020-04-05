"""
IRL you'd probably want to do something like the link below
instead of the sqlite/pandas approach shown here

https://fastapi.tiangolo.com/tutorial/sql-databases/
"""

# %% Imports
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from sqlalchemy import create_engine


# %% Globals
eng = create_engine('sqlite:///data/data.sqlite')
df = pd.read_sql_table('mtcars', eng)
app = FastAPI()


class MtCars(BaseModel):
    name: str
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

    name: Name of Car \n
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


if __name__ == "__main__":
    # For debugging
    # Use editor to place breakpoints then hit API
    # using Postman, FastAPI docs, requests, curl, etc.
    uvicorn.run(app, host="0.0.0.0", port=8000)
