import json
import os
from typing import List, Any, Optional
from jsonpath_ng.ext import parse
from models.jsonpath_models import (
    JsonPathSearchRequest, JsonPathLoadAndSearchRequest,
    JsonPathSearchAllRequest, JsonPathLoadAndSearchAllRequest,
    JsonPathSearchResponse, JsonPathLoadAndSearchResponse,
    JsonPathSearchAllResponse, JsonPathLoadAndSearchAllResponse,
    JsonPathResult
)

class JsonPathService:
    """Service class for JSONPath operations"""
    
    @staticmethod
    def _parse_json_safely(json_string: str) -> tuple[Optional[Any], Optional[str]]:
        """Safely parse JSON string and return data and error"""
        try:
            data = json.loads(json_string)
            return data, None
        except json.JSONDecodeError as e:
            return None, f"Invalid JSON: {str(e)}"
        except Exception as e:
            return None, f"Unexpected error parsing JSON: {str(e)}"
    
    @staticmethod
    def _load_json_file(file_path: str) -> tuple[Optional[Any], Optional[str], Optional[int]]:
        """Load and parse JSON file, return data, error, and file size"""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return None, f"File not found: {file_path}", None
            
            # Check if it's a file (not directory)
            if not os.path.isfile(file_path):
                return None, f"Path is not a file: {file_path}", None
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Read and parse file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                data, parse_error = JsonPathService._parse_json_safely(content)
                
            if parse_error:
                return None, f"Error parsing JSON file: {parse_error}", file_size
                
            return data, None, file_size
            
        except FileNotFoundError:
            return None, f"File not found: {file_path}", None
        except PermissionError:
            return None, f"Permission denied accessing file: {file_path}", None
        except UnicodeDecodeError:
            return None, f"File encoding error. Please ensure file is UTF-8 encoded: {file_path}", None
        except Exception as e:
            return None, f"Unexpected error loading file: {str(e)}", None
    
    @staticmethod
    def _execute_jsonpath(data: Any, jsonpath_expr: str) -> tuple[bool, Optional[List[Any]], Optional[str]]:
        """Execute JSONPath expression and return success, results, and error"""
        try:
            # Parse JSONPath expression
            jsonpath_parsed = parse(jsonpath_expr)
            
            # Find matches
            matches = jsonpath_parsed.find(data)
            
            # Extract values
            if matches:
                result_values = [match.value for match in matches]
                return True, result_values, None
            else:
                return True, [], None
                
        except Exception as e:
            # Handle both parsing errors and execution errors
            error_msg = str(e)
            if "parse" in error_msg.lower() or "syntax" in error_msg.lower():
                return False, None, f"Invalid JSONPath expression: {error_msg}"
            else:
                return False, None, f"Error executing JSONPath: {error_msg}"
    
    def search(self, request: JsonPathSearchRequest) -> JsonPathSearchResponse:
        """Perform JSONPath search on JSON data"""
        try:
            # Parse JSON data
            data, parse_error = self._parse_json_safely(request.json_data)
            if parse_error:
                return JsonPathSearchResponse(
                    success=False,
                    jsonpath=request.jsonpath,
                    matches_found=0,
                    result=None,
                    original_data_size=len(request.json_data),
                    error=parse_error
                )
            
            # Execute JSONPath
            success, results, exec_error = self._execute_jsonpath(data, request.jsonpath)
            if not success:
                return JsonPathSearchResponse(
                    success=False,
                    jsonpath=request.jsonpath,
                    matches_found=0,
                    result=None,
                    original_data_size=len(request.json_data),
                    error=exec_error
                )
            
            # Prepare result - if single match, return the value directly, otherwise return list
            result_data = None
            if results:
                result_data = results[0] if len(results) == 1 else results
            
            return JsonPathSearchResponse(
                success=True,
                jsonpath=request.jsonpath,
                matches_found=len(results),
                result=result_data,
                original_data_size=len(request.json_data)
            )
            
        except Exception as e:
            return JsonPathSearchResponse(
                success=False,
                jsonpath=request.jsonpath,
                matches_found=0,
                result=None,
                original_data_size=len(request.json_data),
                error=f"Unexpected error: {str(e)}"
            )
    
    def load_and_search(self, request: JsonPathLoadAndSearchRequest) -> JsonPathLoadAndSearchResponse:
        """Load JSON file and perform JSONPath search"""
        try:
            # Load JSON file
            data, load_error, file_size = self._load_json_file(request.file_path)
            if load_error:
                return JsonPathLoadAndSearchResponse(
                    success=False,
                    jsonpath=request.jsonpath,
                    file_path=request.file_path,
                    matches_found=0,
                    result=None,
                    file_size_bytes=file_size,
                    error=load_error
                )
            
            # Execute JSONPath
            success, results, exec_error = self._execute_jsonpath(data, request.jsonpath)
            if not success:
                return JsonPathLoadAndSearchResponse(
                    success=False,
                    jsonpath=request.jsonpath,
                    file_path=request.file_path,
                    matches_found=0,
                    result=None,
                    file_size_bytes=file_size,
                    error=exec_error
                )
            
            # Prepare result
            result_data = None
            if results:
                result_data = results[0] if len(results) == 1 else results
            
            return JsonPathLoadAndSearchResponse(
                success=True,
                jsonpath=request.jsonpath,
                file_path=request.file_path,
                matches_found=len(results),
                result=result_data,
                file_size_bytes=file_size
            )
            
        except Exception as e:
            return JsonPathLoadAndSearchResponse(
                success=False,
                jsonpath=request.jsonpath,
                file_path=request.file_path,
                matches_found=0,
                result=None,
                file_size_bytes=None,
                error=f"Unexpected error: {str(e)}"
            )
    
    def search_all(self, request: JsonPathSearchAllRequest) -> JsonPathSearchAllResponse:
        """Perform multiple JSONPath searches on JSON data"""
        try:
            # Parse JSON data
            data, parse_error = self._parse_json_safely(request.json_data)
            if parse_error:
                return JsonPathSearchAllResponse(
                    success=False,
                    total_jsonpaths=len(request.jsonpaths),
                    successful_searches=0,
                    failed_searches=len(request.jsonpaths),
                    results=[],
                    original_data_size=len(request.json_data),
                    error=parse_error
                )
            
            # Execute each JSONPath
            results = []
            successful_count = 0
            failed_count = 0
            
            for jsonpath_expr in request.jsonpaths:
                success, search_results, exec_error = self._execute_jsonpath(data, jsonpath_expr)
                
                if success:
                    successful_count += 1
                    # Prepare result data
                    result_data = None
                    if search_results:
                        result_data = search_results[0] if len(search_results) == 1 else search_results
                    
                    results.append(JsonPathResult(
                        jsonpath=jsonpath_expr,
                        success=True,
                        matches_found=len(search_results),
                        result=result_data
                    ))
                else:
                    failed_count += 1
                    results.append(JsonPathResult(
                        jsonpath=jsonpath_expr,
                        success=False,
                        matches_found=0,
                        result=None,
                        error=exec_error
                    ))
            
            return JsonPathSearchAllResponse(
                success=True,
                total_jsonpaths=len(request.jsonpaths),
                successful_searches=successful_count,
                failed_searches=failed_count,
                results=results,
                original_data_size=len(request.json_data)
            )
            
        except Exception as e:
            return JsonPathSearchAllResponse(
                success=False,
                total_jsonpaths=len(request.jsonpaths),
                successful_searches=0,
                failed_searches=len(request.jsonpaths),
                results=[],
                original_data_size=len(request.json_data),
                error=f"Unexpected error: {str(e)}"
            )
    
    def load_and_search_all(self, request: JsonPathLoadAndSearchAllRequest) -> JsonPathLoadAndSearchAllResponse:
        """Load JSON file and perform multiple JSONPath searches"""
        try:
            # Load JSON file
            data, load_error, file_size = self._load_json_file(request.file_path)
            if load_error:
                return JsonPathLoadAndSearchAllResponse(
                    success=False,
                    file_path=request.file_path,
                    total_jsonpaths=len(request.jsonpaths),
                    successful_searches=0,
                    failed_searches=len(request.jsonpaths),
                    results=[],
                    file_size_bytes=file_size,
                    error=load_error
                )
            
            # Execute each JSONPath
            results = []
            successful_count = 0
            failed_count = 0
            
            for jsonpath_expr in request.jsonpaths:
                success, search_results, exec_error = self._execute_jsonpath(data, jsonpath_expr)
                
                if success:
                    successful_count += 1
                    # Prepare result data
                    result_data = None
                    if search_results:
                        result_data = search_results[0] if len(search_results) == 1 else search_results
                    
                    results.append(JsonPathResult(
                        jsonpath=jsonpath_expr,
                        success=True,
                        matches_found=len(search_results),
                        result=result_data
                    ))
                else:
                    failed_count += 1
                    results.append(JsonPathResult(
                        jsonpath=jsonpath_expr,
                        success=False,
                        matches_found=0,
                        result=None,
                        error=exec_error
                    ))
            
            return JsonPathLoadAndSearchAllResponse(
                success=True,
                file_path=request.file_path,
                total_jsonpaths=len(request.jsonpaths),
                successful_searches=successful_count,
                failed_searches=failed_count,
                results=results,
                file_size_bytes=file_size
            )
            
        except Exception as e:
            return JsonPathLoadAndSearchAllResponse(
                success=False,
                file_path=request.file_path,
                total_jsonpaths=len(request.jsonpaths),
                successful_searches=0,
                failed_searches=len(request.jsonpaths),
                results=[],
                file_size_bytes=file_size,
                error=f"Unexpected error: {str(e)}"
            )
