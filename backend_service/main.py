from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, HTTPException, Request

import requests
import logging
from models import QueryUrl

HEADER = {"accept": "application/vnd.github+json"}

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="basic.log",
    )

app = FastAPI(
    title="Mohamad Denno Backend Coding Challenge",
    description="""
        The service should be able to provide:
        *    A list of the most popular repositories, sorted by number of stars.
        *    An option to be able to view the top 10, 50, 100 repositories should be available.
        *    Given a date, the most popular repositories created from this date onwards should be returned.
        *    A filter for the programming language would be a great addition to have
    """,
    version="0.1.0",
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    json_response =  JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
    logging.info(exc.errors())
    return json_response

@app.get("/")
def root() -> dict[str, str]:
    return {"server": "Running"}

@app.post("/search")
def search(query_params: QueryUrl) -> dict[str, dict[str, str]]:
    
    logging.info(f"The following query {query_params.build_query_url()} being requested")
    
    if all(param is None for param in (query_params.created, query_params.sort, query_params.top_results, query_params.order, query_params.programming_language)):
        raise HTTPException(status_code = 400, detail = "Not enough searching criteria")

    url=query_params.build_query_url()
    response = requests.get(url, headers = HEADER).json()
    results = {repo["name"]: repo["html_url"] for repo in response["items"]}
    return {"repos": results}
