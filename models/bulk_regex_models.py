from pydantic import BaseModel, Field
from typing import List, Optional, Union
from models.regex_models import RegexFlags, RegexMatch, MatchGroup

# Base classes for bulk operations
class BaseBulkRequest(BaseModel):
    """Base request model for bulk regex operations"""
    pattern: str = Field(..., description="Regular expression pattern to apply to all texts")
    texts: List[str] = Field(..., description="List of texts to process")
    flags: Optional[List[RegexFlags]] = Field(default=[], description="Regex flags to apply")

class BulkOperationResult(BaseModel):
    """Result for a single text in bulk operation"""
    text_index: int = Field(description="Index of the text in the original list")
    text: str = Field(description="The original text")
    success: bool = Field(description="Whether the operation succeeded for this text")
    error: Optional[str] = Field(default=None, description="Error message if operation failed")

# Request models for different bulk operations
class BulkMatchRequest(BaseBulkRequest):
    """Request model for bulk regex match operations"""
    pass

class BulkFindAllRequest(BaseBulkRequest):
    """Request model for bulk regex findall operations"""
    pass

class BulkSubstituteRequest(BaseBulkRequest):
    """Request model for bulk regex substitution operations"""
    replacement: str = Field(..., description="Replacement string")
    count: Optional[int] = Field(default=0, description="Maximum number of replacements per text (0 = all)")

class BulkSplitRequest(BaseBulkRequest):
    """Request model for bulk regex split operations"""
    maxsplit: Optional[int] = Field(default=0, description="Maximum number of splits per text (0 = no limit)")

# Result models for specific operations
class BulkMatchResult(BulkOperationResult):
    """Result for bulk match operation on a single text"""
    match: Optional[RegexMatch] = Field(default=None, description="Match result (None if no match)")

class BulkFindAllResult(BulkOperationResult):
    """Result for bulk findall operation on a single text"""
    matches: List[RegexMatch] = Field(default=[], description="All matches found")
    count: int = Field(default=0, description="Number of matches found")

class BulkSubstituteResult(BulkOperationResult):
    """Result for bulk substitute operation on a single text"""
    original_text: str = Field(description="The original text")
    result_text: str = Field(description="The text after substitution")
    substitutions_made: int = Field(default=0, description="Number of substitutions made")

class BulkSplitResult(BulkOperationResult):
    """Result for bulk split operation on a single text"""
    parts: List[str] = Field(default=[], description="The split parts")
    splits_made: int = Field(default=0, description="Number of splits made")

# Base response model for bulk operations
class BaseBulkResponse(BaseModel):
    """Base response model for bulk operations"""
    success: bool = Field(description="Whether the overall operation was successful")
    pattern: str = Field(description="The regex pattern used")
    total_texts: int = Field(description="Total number of texts processed")
    successful_operations: int = Field(description="Number of texts processed successfully")
    failed_operations: int = Field(description="Number of texts that failed to process")
    processing_time_ms: float = Field(description="Total processing time in milliseconds")
    error: Optional[str] = Field(default=None, description="Overall operation error if any")

# Response models for specific operations
class BulkMatchResponse(BaseBulkResponse):
    """Response model for bulk match operations"""
    results: List[BulkMatchResult] = Field(description="Results for each text")

class BulkFindAllResponse(BaseBulkResponse):
    """Response model for bulk findall operations"""
    results: List[BulkFindAllResult] = Field(description="Results for each text")
    total_matches: int = Field(description="Total matches found across all texts")

class BulkSubstituteResponse(BaseBulkResponse):
    """Response model for bulk substitute operations"""
    replacement: str = Field(description="The replacement string used")
    results: List[BulkSubstituteResult] = Field(description="Results for each text")
    total_substitutions: int = Field(description="Total substitutions made across all texts")

class BulkSplitResponse(BaseBulkResponse):
    """Response model for bulk split operations"""
    results: List[BulkSplitResult] = Field(description="Results for each text")
    total_splits: int = Field(description="Total splits made across all texts")
