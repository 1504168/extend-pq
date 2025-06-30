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
   - **Bulk Operations** - Optimized processing for multiple texts

2. **JSONPath Functionality** - Query and filter JSON data via REST API
   - Search JSON data with JSONPath expressions
   - Load and search JSON files
   - Multiple JSONPath queries on single data
   - Batch processing with file loading
   - Complete JSONPath syntax support

### 🔄 Planned
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

## JSONPath API Endpoints

### Base URL: `/jsonpath`

JSONPath is a query language for JSON, similar to XPath for XML. It allows you to extract and filter data from JSON documents using expressions.

#### 1. Search JSON Data
`POST /search` - Search JSON data with JSONPath expression

```json
{
  "json_data": "{\"store\":{\"book\":[{\"title\":\"Book 1\",\"price\":10},{\"title\":\"Book 2\",\"price\":15}]}}",
  "jsonpath": "$.store.book[*].title"
}
```

#### 2. Load and Search JSON File
`POST /load-and-search` - Load JSON file and search with JSONPath

```json
{
  "file_path": "C:\\data\\products.json",
  "jsonpath": "$.products[?(@.price < 50)].name"
}
```

#### 3. Search All (Multiple JSONPaths)
`POST /search-all` - Apply multiple JSONPath expressions to JSON data

```json
{
  "json_data": "{\"users\":[{\"name\":\"John\",\"age\":30},{\"name\":\"Jane\",\"age\":25}]}",
  "jsonpaths": [
    "$.users[*].name",
    "$.users[?(@.age > 25)].name",
    "$.users[0]"
  ]
}
```

#### 4. Load and Search All
`POST /load-and-search-all` - Load JSON file and apply multiple JSONPath expressions

```json
{
  "file_path": "C:\\data\\inventory.json",
  "jsonpaths": [
    "$.products[*].name",
    "$.products[?(@.stock > 0)]",
    "$.categories[*]"
  ]
}
```

#### 5. JSONPath Info
`GET /info` - Get JSONPath syntax help and examples

### JSONPath Syntax Examples

- `$` - Root element
- `$.store.book[*]` - All books in store
- `$.store.book[0]` - First book
- `$.store.book[-1]` - Last book
- `$.store.book[0:2]` - First two books (slice)
- `$.store.book[?(@.price < 10)]` - Books with price less than 10
- `$..author` - All authors (recursive descent)
- `$.store.*` - All things in store

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
│   ├── bulk_regex_models.py   # Bulk regex operations models
│   └── jsonpath_models.py     # JSONPath operations models
├── services/                  # Business logic
│   ├── __init__.py
│   ├── regex_service.py       # Standard regex operations service
│   ├── bulk_regex_service.py  # Bulk regex operations service
│   └── jsonpath_service.py    # JSONPath operations service
├── routes/                    # API endpoints
│   ├── __init__.py
│   ├── regex_routes.py        # Standard regex API routes
│   ├── bulk_regex_routes.py   # Bulk regex operations API routes
│   └── jsonpath_routes.py     # JSONPath operations API routes
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

### JSONPath Operations Example

```python
import requests

# Search JSON data with JSONPath
response = requests.post("http://localhost:8000/jsonpath/search", json={
    "json_data": '{"store":{"book":[{"title":"Book 1","price":10},{"title":"Book 2","price":15}]}}',
    "jsonpath": "$.store.book[*].title"
})

result = response.json()
if result["success"]:
    print(f"Found {result['matches_found']} matches: {result['result']}")

# Load and search JSON file
response = requests.post("http://localhost:8000/jsonpath/load-and-search", json={
    "file_path": "C:\\data\\products.json",
    "jsonpath": "$.products[?(@.price < 50)]"
})

# Multiple JSONPath searches
response = requests.post("http://localhost:8000/jsonpath/search-all", json={
    "json_data": '{"users":[{"name":"John","age":30},{"name":"Jane","age":25}]}',
    "jsonpaths": [
        "$.users[*].name",
        "$.users[?(@.age > 25)].name"
    ]
})

result = response.json()
print(f"Processed {result['total_jsonpaths']} JSONPath expressions")
for res in result['results']:
    if res['success']:
        print(f"JSONPath '{res['jsonpath']}': {res['matches_found']} matches")
```

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

#### JSONPath Operation in Power Query
```powerquery
let
    // Create JSONPath search request
    RequestData = [
        json_data = "{""users"":[{""name"":""John"",""age"":30},{""name"":""Jane"",""age"":25}]}",
        jsonpath = "$.users[*].name"
    ],
    
    // Make the API call
    ApiResponse = Json.Document(Web.Contents("http://localhost:8000/jsonpath/search", [
        Headers = [#"Content-Type"="application/json"],
        Content = Text.ToBinary(Json.FromValue(RequestData))
    ])),
    
    // Extract results
    ExtractedData = if ApiResponse[success] then ApiResponse[result] else null,
    
    // Create final result
    Result = [
        Success = ApiResponse[success],
        JSONPath = ApiResponse[jsonpath],
        MatchesFound = ApiResponse[matches_found],
        Data = ExtractedData,
        ErrorMessage = ApiResponse[error]
    ]
in
    Result
```

#### Load JSON File with JSONPath in Power Query
```powerquery
let
    // Create file load and search request
    RequestData = [
        file_path = "C:\\data\\products.json",
        jsonpath = "$.products[?(@.price < 100)].name"
    ],
    
    // Make the API call
    ApiResponse = Json.Document(Web.Contents("http://localhost:8000/jsonpath/load-and-search", [
        Headers = [#"Content-Type"="application/json"],
        Content = Text.ToBinary(Json.FromValue(RequestData))
    ])),
    
    // Convert result to table if it's a list
    ResultData = if ApiResponse[success] and ApiResponse[result] <> null then
        if Value.Is(ApiResponse[result], type list) then
            Table.FromList(ApiResponse[result], Splitter.SplitByNothing(), {"ProductName"})
        else
            Table.FromRecords({[ProductName = ApiResponse[result]]})
    else
        Table.FromRecords({[Error = ApiResponse[error]]}),
    
    // Add metadata
    FinalResult = Table.AddColumn(ResultData, "Metadata", each [
        FilePath = ApiResponse[file_path],
        MatchesFound = ApiResponse[matches_found],
        FileSizeBytes = ApiResponse[file_size_bytes]
    ])
in
    FinalResult
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
