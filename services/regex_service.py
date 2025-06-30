import re
from typing import List, Optional, Union
from models.regex_models import (
    RegexFlags, RegexMatchRequest, RegexFindAllRequest, RegexSubstituteRequest,
    RegexSplitRequest, RegexValidateRequest, RegexMatch, RegexMatchResponse,
    RegexFindAllResponse, RegexSubstituteResponse, RegexSplitResponse,
    RegexValidateResponse, MatchGroup
)

class RegexService:
    """Service class for regex operations"""
    
    @staticmethod
    def _convert_flags(flags: List[RegexFlags]) -> int:
        """Convert string flags to regex flag constants"""
        flag_map = {
            RegexFlags.IGNORECASE: re.IGNORECASE,
            RegexFlags.MULTILINE: re.MULTILINE,
            RegexFlags.DOTALL: re.DOTALL,
            RegexFlags.VERBOSE: re.VERBOSE,
            RegexFlags.ASCII: re.ASCII,
            RegexFlags.LOCALE: re.LOCALE,
        }
        
        result = 0
        for flag in flags:
            result |= flag_map.get(flag, 0)
        return result
    
    @staticmethod
    def _match_to_model(match_obj: re.Match) -> RegexMatch:
        """Convert regex match object to RegexMatch model"""
        groups = []
        for i, group in enumerate(match_obj.groups()):
            start, end = match_obj.span(i + 1) if i + 1 < len(match_obj.groups()) + 1 else (-1, -1)
            groups.append(MatchGroup(
                group=group,
                start=start,
                end=end
            ))
        
        return RegexMatch(
            match=match_obj.group(0),
            groups=groups,
            start=match_obj.start(),
            end=match_obj.end()
        )
    
    def match(self, request: RegexMatchRequest) -> RegexMatchResponse:
        """Perform regex match operation"""
        try:
            flags = self._convert_flags(request.flags)
            pattern = re.compile(request.pattern, flags)
            match_obj = pattern.search(request.text)
            
            match_result = None
            if match_obj:
                match_result = self._match_to_model(match_obj)
            
            return RegexMatchResponse(
                success=True,
                pattern=request.pattern,
                text=request.text,
                match=match_result
            )
        except re.error as e:
            return RegexMatchResponse(
                success=False,
                pattern=request.pattern,
                text=request.text,
                match=None,
                error=f"Regex error: {str(e)}"
            )
        except Exception as e:
            return RegexMatchResponse(
                success=False,
                pattern=request.pattern,
                text=request.text,
                match=None,
                error=f"Unexpected error: {str(e)}"
            )
    
    def find_all(self, request: RegexFindAllRequest) -> RegexFindAllResponse:
        """Perform regex findall operation"""
        try:
            flags = self._convert_flags(request.flags)
            pattern = re.compile(request.pattern, flags)
            matches = list(pattern.finditer(request.text))
            
            match_results = [self._match_to_model(match) for match in matches]
            
            return RegexFindAllResponse(
                success=True,
                pattern=request.pattern,
                text=request.text,
                matches=match_results,
                count=len(match_results)
            )
        except re.error as e:
            return RegexFindAllResponse(
                success=False,
                pattern=request.pattern,
                text=request.text,
                matches=[],
                count=0,
                error=f"Regex error: {str(e)}"
            )
        except Exception as e:
            return RegexFindAllResponse(
                success=False,
                pattern=request.pattern,
                text=request.text,
                matches=[],
                count=0,
                error=f"Unexpected error: {str(e)}"
            )
    
    def substitute(self, request: RegexSubstituteRequest) -> RegexSubstituteResponse:
        """Perform regex substitution operation"""
        try:
            flags = self._convert_flags(request.flags)
            pattern = re.compile(request.pattern, flags)
            
            result_text, substitutions_made = pattern.subn(
                request.replacement, 
                request.text, 
                count=request.count
            )
            
            return RegexSubstituteResponse(
                success=True,
                pattern=request.pattern,
                replacement=request.replacement,
                original_text=request.text,
                result_text=result_text,
                substitutions_made=substitutions_made
            )
        except re.error as e:
            return RegexSubstituteResponse(
                success=False,
                pattern=request.pattern,
                replacement=request.replacement,
                original_text=request.text,
                result_text=request.text,
                substitutions_made=0,
                error=f"Regex error: {str(e)}"
            )
        except Exception as e:
            return RegexSubstituteResponse(
                success=False,
                pattern=request.pattern,
                replacement=request.replacement,
                original_text=request.text,
                result_text=request.text,
                substitutions_made=0,
                error=f"Unexpected error: {str(e)}"
            )
    
    def split(self, request: RegexSplitRequest) -> RegexSplitResponse:
        """Perform regex split operation"""
        try:
            flags = self._convert_flags(request.flags)
            pattern = re.compile(request.pattern, flags)
            
            parts = pattern.split(request.text, maxsplit=request.maxsplit)
            splits_made = len(parts) - 1
            
            return RegexSplitResponse(
                success=True,
                pattern=request.pattern,
                original_text=request.text,
                parts=parts,
                splits_made=splits_made
            )
        except re.error as e:
            return RegexSplitResponse(
                success=False,
                pattern=request.pattern,
                original_text=request.text,
                parts=[request.text],
                splits_made=0,
                error=f"Regex error: {str(e)}"
            )
        except Exception as e:
            return RegexSplitResponse(
                success=False,
                pattern=request.pattern,
                original_text=request.text,
                parts=[request.text],
                splits_made=0,
                error=f"Unexpected error: {str(e)}"
            )
    
    def validate_pattern(self, request: RegexValidateRequest) -> RegexValidateResponse:
        """Validate regex pattern"""
        try:
            re.compile(request.pattern)
            return RegexValidateResponse(
                success=True,
                pattern=request.pattern,
                valid=True
            )
        except re.error as e:
            return RegexValidateResponse(
                success=True,  # Operation succeeded, but pattern is invalid
                pattern=request.pattern,
                valid=False,
                error=f"Pattern error: {str(e)}"
            )
        except Exception as e:
            return RegexValidateResponse(
                success=False,
                pattern=request.pattern,
                valid=False,
                error=f"Unexpected error: {str(e)}"
            )
