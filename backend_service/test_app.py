from fastapi.testclient import TestClient
from datetime import date
from models import QueryUrl, SortType, TopResultsType, ProgrammingLanguageType, OrderType
from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"server": "Running"}

def test_build_query_url():
    query_params = QueryUrl(
        created =date(2022, 1, 1),
        sort = SortType.STARS,
        top_results = TopResultsType.TOP_10,
        order = OrderType.DESC,
        programming_language = ProgrammingLanguageType.PYTHON,
    )
    expected_url = (
        "https://api.github.com/search/repositories?q=stars:>0+created:>=2022-01-01+language:python&per_page=10&sort=stars&order=desc"
    )
    assert query_params.build_query_url() == expected_url

def test_search_endpoint():
    response = client.post(
        "/search",
        json={
            "created": "2022-01-01",
            "programming_language": "python",
            "top_results": 10,
            "sort": "stars",
            "order": "desc"
        },
    )
    assert response.status_code == 200
    assert "repos" in response.json()

def test_search_endpoint_missing_criteria():
    response = client.post("/search", json={
            "created": None,
            "programming_language": None,
            "top_results": None,
            "sort": None,
            "order": None
        }
    )
    assert response.status_code == 400
    assert "Not enough searching criteria" in response.json()["detail"]


def test_search_invalid_input():
    invalid_input = {
        "created": "invalid_date",
        "sort": "invalid_sort",
        "top_results": "invalid_top",
        "order": "invalid_order",
        "programming_language": "invalid_language"
    }

    response = client.post("/search", json=invalid_input)
    assert response.status_code == 422

def test_search_invalid_logging():
    invalid_input = {
        "programming_language": "RedcareLanguage"
    }

    expected_log = [{'type': 'enum', 'loc': ['body', 'programming_language'], 'msg': "Input should be 'javascript', 'python', 'go', 'java', 'kotlin' or 'php'", 'input': 'RedcareLanguage', 'ctx': {'expected': "'javascript', 'python', 'go', 'java', 'kotlin' or 'php'"}}]

    response = client.post("/search", json=invalid_input)
    assert response.status_code == 422
    assert response.json()["detail"] == expected_log

def test_search_result_number():
    response = client.post(
        "/search",
        json={
            "top_results": 10
        },
    )
    assert response.status_code == 200
    assert 10 == len(response.json()["repos"])
