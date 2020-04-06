
# Fast API Machine Learning Example
ian wuz here

# Overview
## Prereqs

1. Download [ananaconda 3](https://www.anaconda.com/distribution/#download-section)
2. Install `environment.yml` like:
```bash
conda env create -f environment.yml
```
3. Install package
```bash
cd /path/to/repo/
pip install -e .
```

4. Install [vscode](https://code.visualstudio.com/) and/or Jupyter Lab
5. Install [Postman](https://www.postman.com/)

## What is a Rest API?

[This tutorial](https://realpython.com/flask-connexion-rest-api/#what-rest-is) provides a nice overview of Rest APIs. For actually building the API, I prefer `fastapi` (details below) rather than the approach recommended in the article. 

In the wild, Rest APIs are often used to provide people with data from a database (withouth providing access to the actual database). Examples include weather APIs, sports APIs, USA Spending, etc.

Rest APIs are also often used to allow people to embed access to their services into other applications. One such example is [Strava](https://developers.strava.com/) (social fitness app).

Another thing that's becoming popular is deploying ML models as Rest APIs. At larger companies, the ML team might create a model (e.g., marketing model) and a product team might incorporate this model into their product by hitting a Rest API for inference results. One made up example using the Instagram scrolling feed: the IG "feed" team might be sending a user's personal information at an internal Rest API and receiving back an advertisement to place into that user's feed.   


# Accessing RestAPIs

Access from command line:
  - `curl`
  - `wget`
  - `httpie`

Access from GUI:
  - Postman

Access from Python:

- [requests](https://github.com/psf/requests)

## Access Example
Rest API access examples can be found in [access_restapi.ipynb](access_restapi.ipynb)

# Building Rest APIs

## Building Rest APIs in Python

In the cloud, one of the most popular solutions is `AWS Lambda` combined with `AWS API Gateway`. This combo is super cheap, fast, and automatically gives you goodies like load balancing. However, this approach is a bit harder to build/debug locally and it doesn't match up super well with how we usually build things.

Another approach is to use a package like [fastapi](https://fastapi.tiangolo.com/). This package has tons of goodies, including: 1. awesome user documentation, 2. automatic `swagger` (rest api) page creation, and 3. more familiar development style 


This repository contains two `fastapi` APIs:

1. [mtcars_api_sqlite_pd.py](mtcars_api_sqlite_pd.py): This is a very basic example of putting a Rest API in front of a database using `sqlite` and `pandas`. In real life, you'd want to use something more robust like [SQL ORM Link](https://fastapi.tiangolo.com/tutorial/sql-databases/)

You can run this API with: 
```bash
uvicorn mtcars_api_sqlite_pd:app --host 127.0.0.1 --port 8000 --reload
```
2. [iris_model_api.py](iris_model_api.py): This is a very basic example of how an `sklearn` model could be deployed as a Rest API.

You can run this API with:

```
uvicorn iris_model_api:app --host 127.0.0.1 --port 8000 --reload
```

All API docs can be viewed at: `http://localhost:8000/docs`


## Debugging APIs
I personally use `vscode` and follow these [instructions](https://fastapi.tiangolo.com/tutorial/debugging/)

## Testing APIs
The `tests/` directory of this repo contains example `pytest` tests for each API. These tests can be run from the command line using `pytest tests`. They can also be run from an IDE like `vscode` which allows testing and debugging at the same time!!

[vscode debugging & testing](https://code.visualstudio.com/docs/python/testing#_debug-tests)

Note: these tests won't work unless install the packages as editable per the [preqs](##prereqs)


## Deploying Rest APIs

There are lots of options for deploying `fastapi`: https://fastapi.tiangolo.com/deployment/

A basic `docker` approach is shown below:

```docker
FROM continuumio/miniconda3
EXPOSE 8000

# update the base environment rather than making new environment
# for simplicity (must rename `scipaper` to `base` in environment.yml)
COPY environment.yml environment.yml
RUN /opt/conda/bin/conda env update --file environment.yml

# create a user named `restapi` for security
RUN useradd -ms /bin/bash restapi
USER restapi
WORKDIR /home/restapi

# copy in fastapi files
COPY --chown=restapi:restapi restapi.py /home/restapi/restapi.py

# run it!
CMD ["uvicorn","restapi:app","--host","0.0.0.0","--port","8000"]
```

Then you can do:
```bash
cd /path/to/repo
docker build -t restapi .

docker run --rm -it -p 80:8000 restapi
```
Or you can use some fancy service like `AWS Fargate` to run/manage your `docker` containers for you
