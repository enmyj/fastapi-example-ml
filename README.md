
# Scipaper RestAPI
ian wuz here

## Prereqs

1. Download [ananaconda 3](https://www.anaconda.com/distribution/#download-section)
2. Install `environment.yml` like:
```
conda env create -f environment.yml
```
Note: you can also just look at file and install each package yourself into `base` environment like `conda install -y pkg1 pkg1 pkg3` but using a proper environment is good practice

3. Install [VS Code](https://code.visualstudio.com/) and/or Jupyter Lab
4. Install [Postman](https://www.postman.com/)

## What is a Rest API?

[This tutorial](https://realpython.com/flask-connexion-rest-api/#what-rest-is) provides a nice overview of Rest APIs. For actually building the API, I prefer `fastapi` (details below) rather than the approach recommended in the article. 

In the wild, Rest APIs are often used to provide people with data from a database (withouth providing access to the actual database). Examples include weather APIs, sports APIs, USA Spending, etc.

Rest APIs are also often used to allow people to embed access to their services into other applications. One such example is Strava (social fitness app): https://developers.strava.com/

Another thing that's becoming popular is deploying ML models as Rest APIs. At ERI we typically deploy models by writing the inference results to a database with `RADR` or another BI tool pointed at it.   

However, at larger companies, the ML team might create a model (e.g., marketing model) and a product team might incorporate this model into their product by hitting a Rest API for inference results. One made up example using the Instagram scrolling feed: the IG "feed" team might be sending a user's personal information at an internal Rest API and receiving back an advertisement to place into that user's feed.   


## Accessing RestAPIs

Access from command line:
  - `curl`
  - `wget`
  - `httpie`

Access from GUI:
  - Postman

Access from Python:

- [requests](https://github.com/psf/requests)

## Building Rest APIs in Python

In the cloud, one of the most popular solutions is `AWS Lambda` combined with `AWS API Gateway`. This combo is super cheap, fast, and automatically gives you goodies like load balancing. However, this approach is a bit harder to build/debug locally and it doesn't match up super well with how we usually build things.

Another approach is to use a package like `fastapi`: https://fastapi.tiangolo.com/. This package has tons of goodies, including: 1. awesome user documentation, 2. automatic `swagger` (rest api) page creation, and 3. more familiar development style 

Running the example apis locally:
```bash
# mtcars pandas
uvicorn mtcars_api_pd:app --host 127.0.0.1 --port 8000 --reload 
```
API docs can be viewed at: `http://localhost:8000/docs`

## Deploying Rest APIs


There are no doubt more robust solutions, but my simple recommendation would be to use `docker` following this [repo](https://github.com/enmyj/snake):

```docker
FROM continuumio/miniconda3
EXPOSE 8000

# update the base environment rather than making new environment
# for simplicity (must rename in environment.yml)
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
Or you can use some fancy service like `AWS Fargate` to manage your `docker` containers for you