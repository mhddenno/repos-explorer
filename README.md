# Repos-Explorer

## Running with Docker

### Build and run containers

1. Clone the repository and navigate to its directory.

    ```
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Build and run the containers:

    ```
    docker-compose up -d --build
    ```

3. Access the app at [http://localhost:8501/](http://localhost:8501/).

### Stopping containers

```
docker-compose stop
```

### To Run the tests

1. Navigate to the `backend_service` folder.

2. Build the test container:
    ```
    docker build -t test .
    ```

    or from the root with
    ```
    docker build -t test backend_service/.
    ```

3. Run the container with the test
    ```
    docker run --rm -it test pytest
    ```

4. Run the container with coverage test
    ```
    docker run --rm -it test pytest --cov=.
    ```

### To Check the logs

To view logs, navigate to `backend_service/basic.log`

### To Check the service-api docs

-   Access Swagger UI:
    [http://localhost:8000/docs](http://localhost:8000/docs)

-   OpenAPI documentation (JSON):   
    [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

## For local development

### Requirements 
`python 3.10.*`

To set the correct Python version locally, consider using `pyenv` [link](https://github.com/pyenv/pyenv)

### Without docker 

#### Create a virtual environment
`python -m venv venv`

#### Activate the virtual environment
`source venv/bin/activate`

#### Install the requirements
`pip install -r backend_service/requirements.txt`

`pip install -r frontend_service/requirements.txt`

#### Run servers
-   Backend:
`uvicorn backend_service.main:app --reload`

-   Frontend:
`streamlit run frontend_service/stream_lit.py`

#### To Run tests:

`pytest`

#### To Run Coverage Test
`pytest --cov=backend_service`

