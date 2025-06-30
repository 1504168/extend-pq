from fastapi import APIRouter, HTTPException
from models.bulk_regex_models import (
    BulkMatchRequest, BulkFindAllRequest, BulkSubstituteRequest, BulkSplitRequest,
    BulkMatchResponse, BulkFindAllResponse, BulkSubstituteResponse, BulkSplitResponse
)
from services.bulk_regex_service import BulkRegexService

router = APIRouter()
bulk_regex_service = BulkRegexService()

@router.post("/match", response_model=BulkMatchResponse)
async def bulk_regex_match(request: BulkMatchRequest):
    """
    Find the first match of a regex pattern in multiple texts.
    
    Optimized for bulk processing by compiling the pattern once and applying it to all texts.
    Failed operations on individual texts are logged but don't stop processing of other texts.
    
    - **pattern**: Regular expression pattern to apply to all texts
    - **texts**: List of texts to search in
    - **flags**: Optional regex flags (IGNORECASE, MULTILINE, etc.)
    
    Returns results for each text, including successful matches and individual errors.
    """
    return bulk_regex_service.bulk_match(request)

@router.post("/findall", response_model=BulkFindAllResponse)
async def bulk_regex_find_all(request: BulkFindAllRequest):
    """
    Find all matches of a regex pattern in multiple texts.
    
    Optimized for bulk processing by compiling the pattern once and applying it to all texts.
    Failed operations on individual texts are logged but don't stop processing of other texts.
    
    - **pattern**: Regular expression pattern to apply to all texts
    - **texts**: List of texts to search in
    - **flags**: Optional regex flags (IGNORECASE, MULTILINE, etc.)
    
    Returns all matches found in each text, plus total match count across all texts.
    """
    return bulk_regex_service.bulk_find_all(request)

@router.post("/substitute", response_model=BulkSubstituteResponse)
async def bulk_regex_substitute(request: BulkSubstituteRequest):
    """
    Substitute matches of a regex pattern with replacement text in multiple texts.
    
    Optimized for bulk processing by compiling the pattern once and applying it to all texts.
    Failed operations on individual texts are logged but don't stop processing of other texts.
    
    - **pattern**: Regular expression pattern to apply to all texts
    - **replacement**: Replacement string (can include backreferences like \\1, \\2)
    - **texts**: List of texts to perform substitution on
    - **count**: Maximum number of substitutions per text (0 = all occurrences)
    - **flags**: Optional regex flags (IGNORECASE, MULTILINE, etc.)
    
    Returns the substituted text for each input and the number of substitutions made.
    """
    return bulk_regex_service.bulk_substitute(request)

@router.post("/split", response_model=BulkSplitResponse)
async def bulk_regex_split(request: BulkSplitRequest):
    """
    Split multiple texts using a regex pattern as delimiter.
    
    Optimized for bulk processing by compiling the pattern once and applying it to all texts.
    Failed operations on individual texts are logged but don't stop processing of other texts.
    
    - **pattern**: Regular expression pattern to use as delimiter
    - **texts**: List of texts to split
    - **maxsplit**: Maximum number of splits per text (0 = no limit)
    - **flags**: Optional regex flags (IGNORECASE, MULTILINE, etc.)
    
    Returns the split parts for each text and total number of splits made.
    """
    return bulk_regex_service.bulk_split(request)

@router.get("/info")
async def bulk_operations_info():
    """
    Get information about bulk regex operations.
    
    Returns details about available bulk operations, their benefits, and usage recommendations.
    """
    return {
        "description": "Bulk regex operations for processing multiple texts efficiently",
        "benefits": [
            "Pattern compiled once for all texts - significant performance improvement",
            "Individual text failures don't stop processing of other texts",
            "Detailed per-text results with success/failure tracking",
            "Performance metrics including processing time",
            "Aggregated statistics (total matches, substitutions, splits)"
        ],
        "operations": [
            {
                "name": "match",
                "description": "Find first match in each text",
                "endpoint": "/match"
            },
            {
                "name": "findall", 
                "description": "Find all matches in each text",
                "endpoint": "/findall"
            },
            {
                "name": "substitute",
                "description": "Replace matches in each text",
                "endpoint": "/substitute"
            },
            {
                "name": "split",
                "description": "Split each text using pattern",
                "endpoint": "/split"
            }
        ],
        "performance_tips": [
            "Use bulk operations when processing multiple texts with the same pattern",
            "Bulk operations are significantly faster than multiple individual requests",
            "Monitor processing_time_ms in responses to track performance",
            "Consider chunking very large text lists for optimal memory usage"
        ]
    }
