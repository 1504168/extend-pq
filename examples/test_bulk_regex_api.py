"""
Example usage of the Power Query Extensions API - Bulk Regex Operations
Test the bulk regex endpoints with sample data to demonstrate performance benefits
"""
import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000/bulk-regex"

# Sample data for testing
SAMPLE_TEXTS = [
    "Contact us at support@example.com for help",
    "Sales team: sales@company.org and marketing@company.org", 
    "Invalid email: notanemail.com",
    "Multiple emails: john@test.com, jane@test.net, admin@site.gov",
    "No emails in this text at all",
    "Mixed content: Call 123-456-7890 or email info@business.co.uk",
    "Error case: this will work fine",
    "Social media: @username and email contact@social.media",
    "Technical support: tech-support@example-company.com",
    "Empty string: ''",
]

def test_bulk_match():
    """Test bulk regex match endpoint"""
    print("Testing bulk regex match...")
    print("=" * 50)
    
    data = {
        "pattern": r"\b\w+@\w+\.\w+\b",
        "texts": SAMPLE_TEXTS,
        "flags": ["IGNORECASE"]
    }
    
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/bulk-match", json=data)
    request_time = (time.time() - start_time) * 1000
    
    result = response.json()
    
    print(f"Pattern: {result['pattern']}")
    print(f"Total texts processed: {result['total_texts']}")
    print(f"Successful operations: {result['successful_operations']}")
    print(f"Failed operations: {result['failed_operations']}")
    print(f"Server processing time: {result['processing_time_ms']:.2f}ms")
    print(f"Total request time: {request_time:.2f}ms")
    print()
    
    print("Results per text:")
    for i, res in enumerate(result['results']):
        status = "✅" if res['success'] else "❌"
        if res['success'] and res['match']:
            print(f"  {i+1}. {status} Found: '{res['match']['match']}' in '{res['text'][:50]}...'")
        elif res['success']:
            print(f"  {i+1}. {status} No match in '{res['text'][:50]}...'")
        else:
            print(f"  {i+1}. {status} Error: {res['error']}")
    print()

def test_bulk_findall():
    """Test bulk regex findall endpoint"""
    print("Testing bulk regex findall...")
    print("=" * 50)
    
    data = {
        "pattern": r"\b\w+@\w+\.\w+\b",
        "texts": SAMPLE_TEXTS,
        "flags": ["IGNORECASE"]
    }
    
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/bulk-findall", json=data)
    request_time = (time.time() - start_time) * 1000
    
    result = response.json()
    
    print(f"Pattern: {result['pattern']}")
    print(f"Total texts processed: {result['total_texts']}")
    print(f"Total matches found: {result['total_matches']}")
    print(f"Server processing time: {result['processing_time_ms']:.2f}ms")
    print(f"Total request time: {request_time:.2f}ms")
    print()
    
    print("Results per text:")
    for i, res in enumerate(result['results']):
        status = "✅" if res['success'] else "❌"
        if res['success']:
            print(f"  {i+1}. {status} Found {res['count']} matches in '{res['text'][:40]}...'")
            for j, match in enumerate(res['matches']):
                print(f"       - {match['match']}")
        else:
            print(f"  {i+1}. {status} Error: {res['error']}")
    print()

def test_bulk_substitute():
    """Test bulk regex substitute endpoint"""
    print("Testing bulk regex substitute...")
    print("=" * 50)
    
    data = {
        "pattern": r"\b(\w+)@(\w+)\.(\w+)\b",
        "replacement": r"[EMAIL:\1@\2.\3]",
        "texts": SAMPLE_TEXTS,
        "count": 0,
        "flags": ["IGNORECASE"]
    }
    
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/bulk-substitute", json=data)
    request_time = (time.time() - start_time) * 1000
    
    result = response.json()
    
    print(f"Pattern: {result['pattern']}")
    print(f"Replacement: {result['replacement']}")
    print(f"Total substitutions made: {result['total_substitutions']}")
    print(f"Server processing time: {result['processing_time_ms']:.2f}ms")
    print(f"Total request time: {request_time:.2f}ms")
    print()
    
    print("Results per text:")
    for i, res in enumerate(result['results']):
        status = "✅" if res['success'] else "❌"
        if res['success'] and res['substitutions_made'] > 0:
            print(f"  {i+1}. {status} Made {res['substitutions_made']} substitutions:")
            print(f"       Before: {res['original_text']}")
            print(f"       After:  {res['result_text']}")
        elif res['success']:
            print(f"  {i+1}. {status} No substitutions needed: '{res['original_text'][:50]}...'")
        else:
            print(f"  {i+1}. {status} Error: {res['error']}")
    print()

def test_bulk_split():
    """Test bulk regex split endpoint"""
    print("Testing bulk regex split...")
    print("=" * 50)
    
    # Use different sample texts more suitable for splitting
    split_texts = [
        "apple,banana,cherry",
        "one;two;three;four",
        "red|green|blue|yellow|purple",
        "no-delimiters-here",
        "mixed,delimiters;here|and,there",
        "single",
        "trailing,comma,",
        ",leading,comma",
        "multiple,,,commas",
        ""
    ]
    
    data = {
        "pattern": r"[,;|]+",
        "texts": split_texts,
        "maxsplit": 0,
        "flags": []
    }
    
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/bulk-split", json=data)
    request_time = (time.time() - start_time) * 1000
    
    result = response.json()
    
    print(f"Pattern: {result['pattern']}")
    print(f"Total splits made: {result['total_splits']}")
    print(f"Server processing time: {result['processing_time_ms']:.2f}ms")
    print(f"Total request time: {request_time:.2f}ms")
    print()
    
    print("Results per text:")
    for i, res in enumerate(result['results']):
        status = "✅" if res['success'] else "❌"
        if res['success']:
            print(f"  {i+1}. {status} Split '{res['text']}' into {len(res['parts'])} parts:")
            for j, part in enumerate(res['parts']):
                print(f"       {j+1}: '{part}'")
        else:
            print(f"  {i+1}. {status} Error: {res['error']}")
    print()

def test_bulk_info():
    """Test bulk operations info endpoint"""
    print("Testing bulk operations info...")
    print("=" * 50)
    
    response = requests.get(f"{BASE_URL}/bulk-info")
    result = response.json()
    
    print(f"Description: {result['description']}")
    print("\nBenefits:")
    for benefit in result['benefits']:
        print(f"  • {benefit}")
    
    print("\nAvailable operations:")
    for op in result['operations']:
        print(f"  • {op['name']}: {op['description']}")
        print(f"    Endpoint: {op['endpoint']}")
    
    print("\nPerformance tips:")
    for tip in result['performance_tips']:
        print(f"  • {tip}")
    print()

def compare_performance():
    """Compare bulk vs individual operations performance"""
    print("Performance Comparison: Bulk vs Individual Operations")
    print("=" * 60)
    
    # Test data
    test_texts = SAMPLE_TEXTS * 5  # 50 texts total
    pattern = r"\b\w+@\w+\.\w+\b"
    
    # Test bulk operation
    print(f"Testing bulk operation with {len(test_texts)} texts...")
    bulk_data = {
        "pattern": pattern,
        "texts": test_texts,
        "flags": ["IGNORECASE"]
    }
    
    start_time = time.time()
    bulk_response = requests.post(f"{BASE_URL}/bulk-match", json=bulk_data)
    bulk_total_time = (time.time() - start_time) * 1000
    bulk_result = bulk_response.json()
    
    print(f"  Bulk operation total time: {bulk_total_time:.2f}ms")
    print(f"  Server processing time: {bulk_result['processing_time_ms']:.2f}ms")
    print(f"  Successful operations: {bulk_result['successful_operations']}")
    
    # Test individual operations (simulate)
    print(f"\nSimulating {len(test_texts)} individual requests...")
    individual_start = time.time()
    successful_individual = 0
    
    # Test first few individual requests to estimate
    sample_size = min(5, len(test_texts))
    individual_times = []
    
    for i in range(sample_size):
        individual_data = {
            "pattern": pattern,
            "text": test_texts[i],
            "flags": ["IGNORECASE"]
        }
        
        req_start = time.time()
        individual_response = requests.post("http://localhost:8000/regex/match", json=individual_data)
        req_time = (time.time() - req_start) * 1000
        individual_times.append(req_time)
        
        if individual_response.json().get('success'):
            successful_individual += 1
    
    avg_individual_time = sum(individual_times) / len(individual_times)
    estimated_total_individual = avg_individual_time * len(test_texts)
    
    print(f"  Average individual request time: {avg_individual_time:.2f}ms")
    print(f"  Estimated total time for all: {estimated_total_individual:.2f}ms")
    print(f"  Sample successful operations: {successful_individual}/{sample_size}")
    
    # Performance comparison
    print(f"\nPerformance Summary:")
    print(f"  Bulk operation time: {bulk_total_time:.2f}ms")
    print(f"  Estimated individual time: {estimated_total_individual:.2f}ms")
    if estimated_total_individual > 0:
        speedup = estimated_total_individual / bulk_total_time
        print(f"  Speedup factor: {speedup:.1f}x faster")
        print(f"  Time saved: {estimated_total_individual - bulk_total_time:.2f}ms")
    print()

if __name__ == "__main__":
    print("Power Query Extensions API - Bulk Regex Operations Examples")
    print("=" * 70)
    print("Make sure the API server is running at http://localhost:8000")
    print()
    
    try:
        # Test all bulk endpoints
        test_bulk_match()
        test_bulk_findall()
        test_bulk_substitute()
        test_bulk_split()
        test_bulk_info()
        
        # Performance comparison
        compare_performance()
        
        print("🎉 All bulk operations completed successfully!")
        print("📈 Bulk operations provide significant performance benefits for multiple texts")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("   Start the server with: python run.py")
    except Exception as e:
        print(f"❌ Error: {e}")
