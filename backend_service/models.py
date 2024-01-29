from enum import Enum
from pydantic import BaseModel
from datetime import date

BASE_URL = "https://api.github.com/search/repositories"

class SortType(str, Enum):
    """Sorting allowed types"""

    STARS = "stars"
    FORKS = "forks"
    HELPWANTEDISSUES = "help-wanted-issues"
    UPDATED = "updated"

class TopResultsType(int, Enum):
    """Top results allowed types"""

    TOP_10 = 10
    TOP_50 = 50
    TOP_100 = 100

class OrderType(str, Enum):
    """Order allowed types"""

    DESC = "desc"
    ASC = "asc"

class ProgrammingLanguageType(str, Enum):
    """Allowed languages"""

    JAVASCRIPT = "javascript"
    PYTHON = "python"
    GO = "go"
    JAVA = "java"
    KOTLIN = "kotlin"
    PHP = "php"

class QueryUrl(BaseModel):
    """Representation of the allowed query components"""

    created: date | None = None
    sort: SortType | None = SortType.STARS
    top_results: TopResultsType | None = TopResultsType.TOP_10
    order: OrderType | None = None
    programming_language: ProgrammingLanguageType | None = None

    def build_query_url(self) -> str:
        base_component: str = f"{BASE_URL}?q=stars:>0"
        search_component: list[str] = [] 
        query_components: list[str] = []
        
        if self.created is not None:
            search_component.append(f"+created:>={self.created}")

        if self.programming_language is not None:
            search_component.append(f"+language:{self.programming_language}")

        if self.top_results is not None:
            query_components.append(f"&per_page={self.top_results}")

        if self.sort is not None:
            query_components.append(f"&sort={self.sort}")

        if self.order is not None:
            query_components.append(f"&order={self.order}")

        search = "".join(search_component) 
        query = "".join(query_components)
        return base_component + search + query