import re
import time
from typing import List, Optional
from models.bulk_regex_models import (
    BulkMatchRequest, BulkFindAllRequest, BulkSubstituteRequest, BulkSplitRequest,
    BulkMatchResponse, BulkFindAllResponse, BulkSubstituteResponse, BulkSplitResponse,
    BulkMatchResult, BulkFindAllResult, BulkSubstituteResult, BulkSplitResult
)
from models.regex_models import RegexFlags, RegexMatch, MatchGroup
from services.regex_service import RegexService

class BulkRegexService:
    """Service class for bulk regex operations"""
    
    def __init__(self):
        self.regex_service = RegexService()
    
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
    
    def bulk_match(self, request: BulkMatchRequest) -> BulkMatchResponse:
        """Perform bulk regex match operations"""
        start_time = time.time()
        results = []
        successful_operations = 0
        failed_operations = 0
        
        try:
            # Compile pattern once for efficiency
            flags = self._convert_flags(request.flags)
            compiled_pattern = re.compile(request.pattern, flags)
            
            for index, text in enumerate(request.texts):
                try:
                    match_obj = compiled_pattern.search(text)
                    match_result = None
                    if match_obj:
                        match_result = self._match_to_model(match_obj)
                    
                    results.append(BulkMatchResult(
                        text_index=index,
                        text=text,
                        success=True,
                        match=match_result
                    ))
                    successful_operations += 1
                    
                except Exception as e:
                    results.append(BulkMatchResult(
                        text_index=index,
                        text=text,
                        success=False,
                        error=f"Processing error: {str(e)}"
                    ))
                    failed_operations += 1
            
            processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            return BulkMatchResponse(
                success=True,
                pattern=request.pattern,
                total_texts=len(request.texts),
                successful_operations=successful_operations,
                failed_operations=failed_operations,
                processing_time_ms=processing_time,
                results=results
            )
            
        except re.error as e:
            processing_time = (time.time() - start_time) * 1000
            return BulkMatchResponse(
                success=False,
                pattern=request.pattern,
                total_texts=len(request.texts),
                successful_operations=0,
                failed_operations=len(request.texts),
                processing_time_ms=processing_time,
                results=[],
                error=f"Regex pattern error: {str(e)}"
            )
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            return BulkMatchResponse(
                success=False,
                pattern=request.pattern,
                total_texts=len(request.texts),
                successful_operations=0,
                failed_operations=len(request.texts),
                processing_time_ms=processing_time,
                results=[],
                error=f"Unexpected error: {str(e)}"
            )
    
    def bulk_find_all(self, request: BulkFindAllRequest) -> BulkFindAllResponse:
        """Perform bulk regex findall operations"""
        start_time = time.time()
        results = []
        successful_operations = 0
        failed_operations = 0
        total_matches = 0
        
        try:
            # Compile pattern once for efficiency
            flags = self._convert_flags(request.flags)
            compiled_pattern = re.compile(request.pattern, flags)
            
            for index, text in enumerate(request.texts):
                try:
                    matches = list(compiled_pattern.finditer(text))
                    match_results = [self._match_to_model(match) for match in matches]
                    match_count = len(match_results)
                    total_matches += match_count
                    
                    results.append(BulkFindAllResult(
                        text_index=index,
                        text=text,
                        success=True,
                        matches=match_results,
                        count=match_count
                    ))
                    successful_operations += 1
                    
                except Exception as e:
                    results.append(BulkFindAllResult(
                        text_index=index,
                        text=text,
                        success=False,
                        error=f"Processing error: {str(e)}"
                    ))
                    failed_operations += 1
            
            processing_time = (time.time() - start_time) * 1000
            
            return BulkFindAllResponse(
                success=True,
                pattern=request.pattern,
                total_texts=len(request.texts),
                successful_operations=successful_operations,
                failed_operations=failed_operations,
                processing_time_ms=processing_time,
                results=results,
                total_matches=total_matches
            )
            
        except re.error as e:
            processing_time = (time.time() - start_time) * 1000
            return BulkFindAllResponse(
                success=False,
                pattern=request.pattern,
                total_texts=len(request.texts),
                successful_operations=0,
                failed_operations=len(request.texts),
                processing_time_ms=processing_time,
                results=[],
                total_matches=0,
                error=f"Regex pattern error: {str(e)}"
            )
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            return BulkFindAllResponse(
                success=False,
                pattern=request.pattern,
                total_texts=len(request.texts),
                successful_operations=0,
                failed_operations=len(request.texts),
                processing_time_ms=processing_time,
                results=[],
                total_matches=0,
                error=f"Unexpected error: {str(e)}"
            )
    
    def bulk_substitute(self, request: BulkSubstituteRequest) -> BulkSubstituteResponse:
        """Perform bulk regex substitution operations"""
        start_time = time.time()
        results = []
        successful_operations = 0
        failed_operations = 0
        total_substitutions = 0
        
        try:
            # Compile pattern once for efficiency
            flags = self._convert_flags(request.flags)
            compiled_pattern = re.compile(request.pattern, flags)
            
            for index, text in enumerate(request.texts):
                try:
                    result_text, substitutions_made = compiled_pattern.subn(
                        request.replacement, text, count=request.count
                    )
                    total_substitutions += substitutions_made
                    
                    results.append(BulkSubstituteResult(
                        text_index=index,
                        text=text,
                        success=True,
                        original_text=text,
                        result_text=result_text,
                        substitutions_made=substitutions_made
                    ))
                    successful_operations += 1
                    
                except Exception as e:
                    results.append(BulkSubstituteResult(
                        text_index=index,
                        text=text,
                        success=False,
                        original_text=text,
                        result_text=text,  # Return original text on error
                        error=f"Processing error: {str(e)}"
                    ))
                    failed_operations += 1
            
            processing_time = (time.time() - start_time) * 1000
            
            return BulkSubstituteResponse(
                success=True,
                pattern=request.pattern,
                replacement=request.replacement,
                total_texts=len(request.texts),
                successful_operations=successful_operations,
                failed_operations=failed_operations,
                processing_time_ms=processing_time,
                results=results,
                total_substitutions=total_substitutions
            )
            
        except re.error as e:
            processing_time = (time.time() - start_time) * 1000
            return BulkSubstituteResponse(
                success=False,
                pattern=request.pattern,
                replacement=request.replacement,
                total_texts=len(request.texts),
                successful_operations=0,
                failed_operations=len(request.texts),
                processing_time_ms=processing_time,
                results=[],
                total_substitutions=0,
                error=f"Regex pattern error: {str(e)}"
            )
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            return BulkSubstituteResponse(
                success=False,
                pattern=request.pattern,
                replacement=request.replacement,
                total_texts=len(request.texts),
                successful_operations=0,
                failed_operations=len(request.texts),
                processing_time_ms=processing_time,
                results=[],
                total_substitutions=0,
                error=f"Unexpected error: {str(e)}"
            )
    
    def bulk_split(self, request: BulkSplitRequest) -> BulkSplitResponse:
        """Perform bulk regex split operations"""
        start_time = time.time()
        results = []
        successful_operations = 0
        failed_operations = 0
        total_splits = 0
        
        try:
            # Compile pattern once for efficiency
            flags = self._convert_flags(request.flags)
            compiled_pattern = re.compile(request.pattern, flags)
            
            for index, text in enumerate(request.texts):
                try:
                    parts = compiled_pattern.split(text, maxsplit=request.maxsplit)
                    splits_made = len(parts) - 1
                    total_splits += splits_made
                    
                    results.append(BulkSplitResult(
                        text_index=index,
                        text=text,
                        success=True,
                        parts=parts,
                        splits_made=splits_made
                    ))
                    successful_operations += 1
                    
                except Exception as e:
                    results.append(BulkSplitResult(
                        text_index=index,
                        text=text,
                        success=False,
                        parts=[text],  # Return original text as single part on error
                        error=f"Processing error: {str(e)}"
                    ))
                    failed_operations += 1
            
            processing_time = (time.time() - start_time) * 1000
            
            return BulkSplitResponse(
                success=True,
                pattern=request.pattern,
                total_texts=len(request.texts),
                successful_operations=successful_operations,
                failed_operations=failed_operations,
                processing_time_ms=processing_time,
                results=results,
                total_splits=total_splits
            )
            
        except re.error as e:
            processing_time = (time.time() - start_time) * 1000
            return BulkSplitResponse(
                success=False,
                pattern=request.pattern,
                total_texts=len(request.texts),
                successful_operations=0,
                failed_operations=len(request.texts),
                processing_time_ms=processing_time,
                results=[],
                total_splits=0,
                error=f"Regex pattern error: {str(e)}"
            )
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            return BulkSplitResponse(
                success=False,
                pattern=request.pattern,
                total_texts=len(request.texts),
                successful_operations=0,
                failed_operations=len(request.texts),
                processing_time_ms=processing_time,
                results=[],
                total_splits=0,
                error=f"Unexpected error: {str(e)}"
            )
