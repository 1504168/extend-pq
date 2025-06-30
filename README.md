# extend-pq
Extend Power Query capabilities using Python as backend system

A FastAPI-based backend service that provides advanced text processing capabilities through HTTP endpoints, specifically designed to extend Power Query functionality.

## Features

### ✅ Implemented
1. **Regex Functionality** - Complete regex operations via REST API
   - Pattern matching
   - Find all matches
   - Text substitution with backreferences
   - Text splitting
   - Pattern validation
   - Support for all standard regex flags
   - **NEW: Bulk Operations** - Optimized processing for multiple texts

### 🔄 Planned
2. JSONPath
3. XPath  
4. HTML Selector Functionality
5. Fuzzy Match

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd extend-pq
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## Regex API Endpoints

### Standard Operations
#### Base URL: `/regex`

#### 1. Pattern Matching
`POST /match` - Find the first match of a pattern

```json
{
  "pattern": "\\b\\w+@\\w+\\.\\w+\\b",
  "text": "Contact us at support@example.com",
  "flags": ["IGNORECASE"]
}
```

#### 2. Find All Matches
`POST /findall` - Find all matches of a pattern

```json
{
  "pattern": "\\d+",
  "text": "There are 123 apples and 456 oranges",
  "flags": []
}
```

#### 3. Text Substitution
`POST /substitute` - Replace matches with replacement text

```json
{
  "pattern": "(\\w+)@(\\w+)\\.(\\w+)",
  "replacement": "[EMAIL: \\1 at \\2 dot \\3]",
  "text": "Contact support@example.com",
  "count": 0,
  "flags": ["IGNORECASE"]
}
```

#### 4. Text Splitting
`POST /split` - Split text using regex pattern

```json
{
  "pattern": "[,;]\\s*",
  "text": "apple, banana; cherry, date",
  "maxsplit": 0,
  "flags": []
}
```

#### 5. Pattern Validation
`POST /validate` - Validate regex pattern syntax

```json
{
  "pattern": "\\b\\w+@\\w+\\.\\w+\\b"
}
```

#### 6. Available Flags
`GET /flags` - Get list of supported regex flags

## Supported Regex Flags

- `IGNORECASE` - Case-insensitive matching
- `MULTILINE` - ^ and $ match start/end of each line
- `DOTALL` - . matches any character including newline
- `VERBOSE` - Allow verbose regex with comments
- `ASCII` - ASCII-only matching for \\w, \\d, \\s
- `LOCALE` - Locale-dependent matching

### Bulk Operations (⚡ High Performance)
#### Base URL: `/regex/bulk`

Optimized for processing multiple texts with the same pattern. The regex pattern is compiled once and applied to all texts, providing significant performance improvements.

#### 1. Bulk Pattern Matching
`POST /match` - Find first match in multiple texts

```json
{
  "pattern": "\\b\\w+@\\w+\\.\\w+\\b",
  "texts": [
    "Email me at john@example.com",
    "Contact support@company.org",
    "No email here"
  ],
  "flags": ["IGNORECASE"]
}
```

#### 2. Bulk Find All Matches
`POST /findall` - Find all matches in multiple texts

```json
{
  "pattern": "\\d+",
  "texts": [
    "Room 123 and 456",
    "No numbers here",
    "Years: 2023, 2024, 2025"
  ],
  "flags": []
}
```

#### 3. Bulk Text Substitution
`POST /substitute` - Replace matches in multiple texts

```json
{
  "pattern": "(\\w+)@(\\w+)\\.(\\w+)",
  "replacement": "[EMAIL: \\1 at \\2 dot \\3]",
  "texts": [
    "Contact john@example.com",
    "Email support@company.org"
  ],
  "count": 0,
  "flags": ["IGNORECASE"]
}
```

#### 4. Bulk Text Splitting
`POST /split` - Split multiple texts using regex pattern

```json
{
  "pattern": "[,;]\\s*",
  "texts": [
    "apple, banana, cherry",
    "red; green; blue",
    "single-item"
  ],
  "maxsplit": 0,
  "flags": []
}
```

#### 5. Bulk Operations Info
`GET /info` - Get information about bulk operations

### 🚀 Performance Benefits

- **Pattern Compilation**: Regex compiled once for all texts
- **Error Isolation**: Individual text failures don't stop processing
- **Detailed Tracking**: Per-text success/failure status
- **Performance Metrics**: Processing time measurement
- **Aggregated Statistics**: Total matches, substitutions, splits across all texts

**Performance Example**: Processing 100 texts is typically 5-10x faster using bulk operations compared to 100 individual requests.

## Project Structure

```
extend-pq/
├── main.py                    # FastAPI application entry point
├── run.py                     # Server startup script
├── requirements.txt           # Python dependencies
├── models/                    # Pydantic data models
│   ├── __init__.py
│   ├── regex_models.py        # Standard regex request/response models
│   └── bulk_regex_models.py   # Bulk operations models
├── services/                  # Business logic
│   ├── __init__.py
│   ├── regex_service.py       # Standard regex operations service
│   └── bulk_regex_service.py  # Bulk operations service
├── routes/                    # API endpoints
│   ├── __init__.py
│   ├── regex_routes.py        # Standard regex API routes
│   └── bulk_regex_routes.py   # Bulk operations API routes
└── examples/                  # Usage examples
    ├── test_regex_api.py      # Standard API testing examples
    └── test_bulk_regex_api.py # Bulk operations testing examples
```

## Usage Examples

### Python Client Example

```python
import requests

# Test regex match
response = requests.post("http://localhost:8000/regex/match", json={
    "pattern": r"\b\w+@\w+\.\w+\b",
    "text": "Email me at john@example.com",
    "flags": ["IGNORECASE"]
})

result = response.json()
if result["match"]:
    print(f"Found email: {result['match']['match']}")
```

### Bulk Operations Example

```python
import requests

# Process multiple texts with one API call
response = requests.post("http://localhost:8000/regex/bulk/match", json={
    "pattern": r"\b\w+@\w+\.\w+\b",
    "texts": [
        "Email me at john@example.com",
        "Contact support@company.org", 
        "No email in this text"
    ],
    "flags": ["IGNORECASE"]
})

result = response.json()
print(f"Processed {result['total_texts']} texts in {result['processing_time_ms']}ms")
print(f"Successful: {result['successful_operations']}, Failed: {result['failed_operations']}")

for res in result['results']:
    if res['success'] and res['match']:
        print(f"Found: {res['match']['match']} in text {res['text_index']}")
```

### Power Query Integration

You can call these endpoints from Power Query using `Web.Contents()`:

#### Standard Regex Operation
```powerquery
let
    // Create the request payload
    RequestData = [
        pattern = "\b\w+@\w+\.\w+\b",
        text = "Contact support@example.com",
        flags = {"IGNORECASE"}
    ],
    
    // Convert to JSON and make the API call
    Source = Json.Document(Web.Contents("http://localhost:8000/regex/match", [
        Headers = [#"Content-Type"="application/json"],
        Content = Text.ToBinary(Json.FromValue(RequestData))
    ]))
in
    Source
```

#### Bulk Regex Operation
```powerquery
let
    // Create the request payload for bulk operation
    RequestData = [
        pattern = "\b\w+@\w+\.\w+\b",
        texts = {"Contact support@example.com", "Email sales@company.org", "No email here"},
        flags = {"IGNORECASE"}
    ],
    
    // Convert to JSON and make the API call
    Source = Json.Document(Web.Contents("http://localhost:8000/regex/bulk/match", [
        Headers = [#"Content-Type"="application/json"],
        Content = Text.ToBinary(Json.FromValue(RequestData))
    ]))
in
    Source
```

#### Processing Results in Power Query
```powerquery
let
    // Create the request payload
    RequestData = [
        pattern = "\b\w+@\w+\.\w+\b",
        text = "Contact support@example.com",
        flags = {"IGNORECASE"}
    ],
    
    // Make the API call
    ApiResponse = Json.Document(Web.Contents("http://localhost:8000/regex/match", [
        Headers = [#"Content-Type"="application/json"],
        Content = Text.ToBinary(Json.FromValue(RequestData))
    ])),
    
    // Extract the match result
    MatchFound = if ApiResponse[success] and ApiResponse[match] <> null 
                 then ApiResponse[match][match] 
                 else null,
    
    // Create final result
    Result = [
        Success = ApiResponse[success],
        Pattern = ApiResponse[pattern],
        InputText = ApiResponse[text],
        MatchedText = MatchFound,
        ErrorMessage = ApiResponse[error]
    ]
in
    Result
```

## Development

### Adding New Functionality

The project is structured to easily add new capabilities:

1. **Models**: Add request/response models in `models/` package
2. **Services**: Add business logic in `services/` package  
3. **Routes**: Add API endpoints in `routes/` package
4. **Integration**: Register routes in `main.py`

### Environment Configuration

Copy `.env.example` to `.env` and adjust settings as needed.

## API Response Format

All endpoints return structured responses with:
- `success`: Operation success status
- `error`: Error message (if any)
- Operation-specific data fields

Example response:
```json
{
  "success": true,
  "pattern": "\\d+",
  "text": "123 apples",
  "match": {
    "match": "123",
    "groups": [],
    "start": 0,
    "end": 3
  },
  "error": null
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your functionality following the existing patterns
4. Test your changes
5. Submit a pull request

## License

[Add your license information here]
