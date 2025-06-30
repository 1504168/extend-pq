from pydantic import BaseModel, Field
from typing import List, Optional, Any, Union
import json

# Base classes for JSONPath operations
class BaseJsonPathRequest(BaseModel):
    """Base request model with common JSONPath fields"""
    jsonpath: str = Field(..., description="JSONPath expression to evaluate")

class BaseJsonPathResponse(BaseModel):
    """Base response model with common response fields"""
    success: bool = Field(description="Whether the operation was successful")
    jsonpath: str = Field(description="The JSONPath expression used")
    error: Optional[str] = Field(default=None, description="Error message if operation failed")

# Request models for JSONPath operations
class JsonPathSearchRequest(BaseJsonPathRequest):
    """Request model for JSONPath search operation"""
    json_data: str = Field(..., description="JSON data as string to search in")

class JsonPathLoadAndSearchRequest(BaseJsonPathRequest):
    """Request model for JSONPath load and search operation"""
    file_path: str = Field(..., description="Absolute path to JSON file to load and search")

class JsonPathSearchAllRequest(BaseModel):
    """Request model for JSONPath search all operation"""
    json_data: str = Field(..., description="JSON data as string to search in")
    jsonpaths: List[str] = Field(..., description="List of JSONPath expressions to evaluate")

class JsonPathLoadAndSearchAllRequest(BaseModel):
    """Request model for JSONPath load and search all operation"""
    file_path: str = Field(..., description="Absolute path to JSON file to load and search")
    jsonpaths: List[str] = Field(..., description="List of JSONPath expressions to evaluate")

# Result models
class JsonPathResult(BaseModel):
    """Model for a single JSONPath search result"""
    jsonpath: str = Field(description="The JSONPath expression used")
    success: bool = Field(description="Whether this specific search was successful")
    matches_found: int = Field(description="Number of matches found")
    result: Optional[Any] = Field(description="The matched data (can be any JSON type)")
    error: Optional[str] = Field(default=None, description="Error message if this search failed")

# Response models
class JsonPathSearchResponse(BaseJsonPathResponse):
    """Response model for JSONPath search operation"""
    matches_found: int = Field(description="Number of matches found")
    result: Optional[Any] = Field(description="The matched data (can be any JSON type)")
    original_data_size: int = Field(description="Size of original JSON data in characters")

class JsonPathLoadAndSearchResponse(BaseJsonPathResponse):
    """Response model for JSONPath load and search operation"""
    file_path: str = Field(description="The file path that was loaded")
    matches_found: int = Field(description="Number of matches found")
    result: Optional[Any] = Field(description="The matched data (can be any JSON type)")
    file_size_bytes: Optional[int] = Field(default=None, description="Size of loaded file in bytes")

class JsonPathSearchAllResponse(BaseModel):
    """Response model for JSONPath search all operation"""
    success: bool = Field(description="Whether the overall operation was successful")
    total_jsonpaths: int = Field(description="Total number of JSONPath expressions processed")
    successful_searches: int = Field(description="Number of successful searches")
    failed_searches: int = Field(description="Number of failed searches")
    results: List[JsonPathResult] = Field(description="Results for each JSONPath expression")
    original_data_size: int = Field(description="Size of original JSON data in characters")
    error: Optional[str] = Field(default=None, description="Overall operation error if any")

class JsonPathLoadAndSearchAllResponse(BaseModel):
    """Response model for JSONPath load and search all operation"""
    success: bool = Field(description="Whether the overall operation was successful")
    file_path: str = Field(description="The file path that was loaded")
    total_jsonpaths: int = Field(description="Total number of JSONPath expressions processed")
    successful_searches: int = Field(description="Number of successful searches")
    failed_searches: int = Field(description="Number of failed searches")
    results: List[JsonPathResult] = Field(description="Results for each JSONPath expression")
    file_size_bytes: Optional[int] = Field(default=None, description="Size of loaded file in bytes")
    error: Optional[str] = Field(default=None, description="Overall operation error if any")
