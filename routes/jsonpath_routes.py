from fastapi import APIRouter, HTTPException
from models.jsonpath_models import (
    JsonPathSearchRequest, JsonPathLoadAndSearchRequest,
    JsonPathSearchAllRequest, JsonPathLoadAndSearchAllRequest,
    JsonPathSearchResponse, JsonPathLoadAndSearchResponse,
    JsonPathSearchAllResponse, JsonPathLoadAndSearchAllResponse
)
from services.jsonpath_service import JsonPathService

router = APIRouter()
jsonpath_service = JsonPathService()

@router.post("/search", response_model=JsonPathSearchResponse)
async def jsonpath_search(request: JsonPathSearchRequest):
    """
    Search for a specific JSONPath in JSON data and return filtered results.
    
    - **json_data**: JSON data as string to search in
    - **jsonpath**: JSONPath expression to evaluate (e.g., "$.store.book[0].title")
    
    Returns the matched data. If multiple matches are found, returns a list.
    If single match is found, returns the value directly.
    """
    return jsonpath_service.search(request)

@router.post("/load-and-search", response_model=JsonPathLoadAndSearchResponse)
async def jsonpath_load_and_search(request: JsonPathLoadAndSearchRequest):
    """
    Load a JSON file and search for a specific JSONPath, returning filtered results.
    
    - **file_path**: Absolute path to JSON file to load and search
    - **jsonpath**: JSONPath expression to evaluate (e.g., "$.users[*].name")
    
    The backend system loads the file and runs the JSONPath expression.
    Returns the matched data along with file information.
    """
    return jsonpath_service.load_and_search(request)

@router.post("/search-all", response_model=JsonPathSearchAllResponse)
async def jsonpath_search_all(request: JsonPathSearchAllRequest):
    """
    Search for multiple JSONPath expressions in JSON data and return all results.
    
    - **json_data**: JSON data as string to search in
    - **jsonpaths**: List of JSONPath expressions to evaluate
    
    Returns results for each JSONPath expression. Failed searches for individual
    expressions are logged but don't stop processing of other expressions.
    """
    return jsonpath_service.search_all(request)

@router.post("/load-and-search-all", response_model=JsonPathLoadAndSearchAllResponse)
async def jsonpath_load_and_search_all(request: JsonPathLoadAndSearchAllRequest):
    """
    Load a JSON file and search for multiple JSONPath expressions, returning all results.
    
    - **file_path**: Absolute path to JSON file to load and search
    - **jsonpaths**: List of JSONPath expressions to evaluate
    
    The backend system loads the file once and runs all JSONPath expressions.
    Returns results for each expression along with file information.
    """
    return jsonpath_service.load_and_search_all(request)

@router.get("/info")
async def jsonpath_operations_info():
    """
    Get information about JSONPath operations and syntax examples.
    
    Returns details about available operations, JSONPath syntax, and usage examples.
    """
    return {
        "description": "JSONPath operations for querying and filtering JSON data",
        "operations": [
            {
                "name": "search",
                "description": "Search JSON data with a single JSONPath expression",
                "endpoint": "/search"
            },
            {
                "name": "load-and-search",
                "description": "Load JSON file and search with a single JSONPath expression",
                "endpoint": "/load-and-search"
            },
            {
                "name": "search-all",
                "description": "Search JSON data with multiple JSONPath expressions",
                "endpoint": "/search-all"
            },
            {
                "name": "load-and-search-all",
                "description": "Load JSON file and search with multiple JSONPath expressions",
                "endpoint": "/load-and-search-all"
            }
        ],
        "jsonpath_syntax": {
            "description": "JSONPath syntax for querying JSON data",
            "examples": [
                {
                    "expression": "$",
                    "description": "Root element"
                },
                {
                    "expression": "$.store.book[*]",
                    "description": "All books in store"
                },
                {
                    "expression": "$.store.book[0]",
                    "description": "First book"
                },
                {
                    "expression": "$.store.book[-1]",
                    "description": "Last book"
                },
                {
                    "expression": "$.store.book[0,1]",
                    "description": "First two books"
                },
                {
                    "expression": "$.store.book[0:2]",
                    "description": "First two books (slice)"
                },
                {
                    "expression": "$.store.book[?(@.price < 10)]",
                    "description": "Books with price less than 10"
                },
                {
                    "expression": "$..author",
                    "description": "All authors (recursive descent)"
                },
                {
                    "expression": "$.store.book[*].author",
                    "description": "Authors of all books"
                },
                {
                    "expression": "$.store.*",
                    "description": "All things in store"
                }
            ]
        },
        "common_use_cases": [
            "Extract specific fields from complex JSON responses",
            "Filter arrays based on conditions", 
            "Navigate nested object structures",
            "Aggregate data from multiple sources",
            "Transform JSON data for reporting"
        ],
        "performance_tips": [
            "Use specific paths instead of recursive descent when possible",
            "Load files once and use search-all for multiple queries",
            "Consider file size when loading large JSON files",
            "Use appropriate JSONPath expressions to minimize result size"
        ]
    }
