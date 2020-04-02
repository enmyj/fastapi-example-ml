import pandas as pd
from sqlalchemy import create_engine

eng = create_engine('sqlite:///./data.sqlite')

df = pd.read_csv('iris.csv')
df.to_sql('iris', eng, index=False, if_exists='replace')

df = pd.read_csv('mtcars.csv')
df.to_sql('mtcars', eng, index=False, if_exists='replace')
