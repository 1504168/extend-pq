from fastapi import APIRouter, HTTPException
from models.regex_models import (
    RegexMatchRequest, RegexFindAllRequest, RegexSubstituteRequest,
    RegexSplitRequest, RegexValidateRequest, RegexMatchResponse,
    RegexFindAllResponse, RegexSubstituteResponse, RegexSplitResponse,
    RegexValidateResponse
)
from services.regex_service import RegexService

router = APIRouter()
regex_service = RegexService()

@router.post("/match", response_model=RegexMatchResponse)
async def regex_match(request: RegexMatchRequest):
    """
    Find the first match of a regex pattern in text.
    
    - **pattern**: Regular expression pattern
    - **text**: Text to search in
    - **flags**: Optional regex flags (IGNORECASE, MULTILINE, etc.)
    
    Returns the first match found, or None if no match.
    """
    return regex_service.match(request)

@router.post("/findall", response_model=RegexFindAllResponse)
async def regex_find_all(request: RegexFindAllRequest):
    """
    Find all matches of a regex pattern in text.
    
    - **pattern**: Regular expression pattern
    - **text**: Text to search in
    - **flags**: Optional regex flags (IGNORECASE, MULTILINE, etc.)
    
    Returns all matches found.
    """
    return regex_service.find_all(request)

@router.post("/substitute", response_model=RegexSubstituteResponse)
async def regex_substitute(request: RegexSubstituteRequest):
    """
    Substitute matches of a regex pattern with replacement text.
    
    - **pattern**: Regular expression pattern
    - **replacement**: Replacement string (can include backreferences like \\1, \\2)
    - **text**: Text to perform substitution on
    - **count**: Maximum number of substitutions (0 = all occurrences)
    - **flags**: Optional regex flags (IGNORECASE, MULTILINE, etc.)
    
    Returns the text after substitution and the number of substitutions made.
    """
    return regex_service.substitute(request)

@router.post("/split", response_model=RegexSplitResponse)
async def regex_split(request: RegexSplitRequest):
    """
    Split text using a regex pattern as delimiter.
    
    - **pattern**: Regular expression pattern to use as delimiter
    - **text**: Text to split
    - **maxsplit**: Maximum number of splits (0 = no limit)
    - **flags**: Optional regex flags (IGNORECASE, MULTILINE, etc.)
    
    Returns the split parts.
    """
    return regex_service.split(request)

@router.post("/validate", response_model=RegexValidateResponse)
async def regex_validate(request: RegexValidateRequest):
    """
    Validate a regex pattern for syntax correctness.
    
    - **pattern**: Regular expression pattern to validate
    
    Returns whether the pattern is syntactically correct.
    """
    return regex_service.validate_pattern(request)

@router.get("/flags")
async def get_available_flags():
    """
    Get list of available regex flags.
    
    Returns all available regex flags that can be used in operations.
    """
    return {
        "flags": [
            {
                "name": "IGNORECASE",
                "description": "Perform case-insensitive matching"
            },
            {
                "name": "MULTILINE", 
                "description": "^ and $ match start/end of each line"
            },
            {
                "name": "DOTALL",
                "description": ". matches any character including newline"
            },
            {
                "name": "VERBOSE",
                "description": "Allow verbose regex with comments and whitespace"
            },
            {
                "name": "ASCII",
                "description": "Make \\w, \\W, \\b, \\B, \\d, \\D, \\s, \\S match ASCII only"
            },
            {
                "name": "LOCALE",
                "description": "Make \\w, \\W, \\b, \\B dependent on current locale"
            }
        ]
    }
