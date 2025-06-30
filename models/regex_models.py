from pydantic import BaseModel, Field
from typing import List, Optional, Union
from enum import Enum

class RegexFlags(str, Enum):
    """Regex flags enumeration"""
    IGNORECASE = "IGNORECASE"
    MULTILINE = "MULTILINE"
    DOTALL = "DOTALL"
    VERBOSE = "VERBOSE"
    ASCII = "ASCII"
    LOCALE = "LOCALE"

# Base classes for common fields
class BaseRegexRequest(BaseModel):
    """Base request model with common regex fields"""
    pattern: str = Field(..., description="Regular expression pattern")
    flags: Optional[List[RegexFlags]] = Field(default=[], description="Regex flags to apply")

class BaseTextRequest(BaseRegexRequest):
    """Base request model with pattern, flags, and text fields"""
    text: str = Field(..., description="Text to process")

class BaseRegexResponse(BaseModel):
    """Base response model with common response fields"""
    success: bool = Field(description="Whether the operation was successful")
    pattern: str = Field(description="The regex pattern used")
    error: Optional[str] = Field(default=None, description="Error message if operation failed")

class BaseTextResponse(BaseRegexResponse):
    """Base response model with pattern and text fields"""
    text: str = Field(description="The input text")

# Request models using inheritance
class RegexMatchRequest(BaseTextRequest):
    """Request model for regex match operations"""
    pass

class RegexFindAllRequest(BaseTextRequest):
    """Request model for regex findall operations"""
    pass

class RegexSubstituteRequest(BaseTextRequest):
    """Request model for regex substitution operations"""
    replacement: str = Field(..., description="Replacement string")
    count: Optional[int] = Field(default=0, description="Maximum number of replacements (0 = all)")

class RegexSplitRequest(BaseTextRequest):
    """Request model for regex split operations"""
    maxsplit: Optional[int] = Field(default=0, description="Maximum number of splits (0 = no limit)")

class RegexValidateRequest(BaseRegexRequest):
    """Request model for regex pattern validation"""
    pass

class MatchGroup(BaseModel):
    """Model for regex match groups"""
    group: Optional[str] = Field(description="Matched group content")
    start: int = Field(description="Start position of the match")
    end: int = Field(description="End position of the match")

class RegexMatch(BaseModel):
    """Model for regex match result"""
    match: Optional[str] = Field(description="Full matched string")
    groups: List[MatchGroup] = Field(description="Captured groups")
    start: int = Field(description="Start position of the full match")
    end: int = Field(description="End position of the full match")

class RegexMatchResponse(BaseTextResponse):
    """Response model for regex match operations"""
    match: Optional[RegexMatch] = Field(description="Match result (None if no match)")

class RegexFindAllResponse(BaseTextResponse):
    """Response model for regex findall operations"""
    matches: List[RegexMatch] = Field(description="All matches found")
    count: int = Field(description="Number of matches found")

class RegexSubstituteResponse(BaseRegexResponse):
    """Response model for regex substitution operations"""
    replacement: str = Field(description="The replacement string used")
    original_text: str = Field(description="The original text")
    result_text: str = Field(description="The text after substitution")
    substitutions_made: int = Field(description="Number of substitutions made")

class RegexSplitResponse(BaseRegexResponse):
    """Response model for regex split operations"""
    original_text: str = Field(description="The original text")
    parts: List[str] = Field(description="The split parts")
    splits_made: int = Field(description="Number of splits made")

class RegexValidateResponse(BaseRegexResponse):
    """Response model for regex pattern validation"""
    valid: bool = Field(description="Whether the pattern is syntactically correct")
