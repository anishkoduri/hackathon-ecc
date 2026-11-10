---
name: api-integration
description: Design and implement REST API integrations with proper error handling, authentication, rate limiting, and testing. Use when building API clients, integrating third-party services, or when users mention API, REST, webhooks, HTTP requests, or service integration. For a named API, tool, or SDK, use integration first — this skill owns generic REST-client mechanics on an unnamed API.
license: MIT
metadata:
  author: agent-skills-demo
  version: "1.0"
  category: integration
compatibility: Requires Python 3.8+ with requests library
---

# API Integration Skill

## When to Use This Skill

Use this skill when:
- Building a client to consume a REST API
- Integrating third-party services on an UNNAMED/generic API (for a named API like Stripe or Twilio, use integration first)
- Implementing webhooks
- Creating or testing HTTP endpoints
- Users mention "API", "REST", "integration", "webhook", or "HTTP"

## Integration Process

### 1. API Discovery & Planning

**Understand the API:**
- Review API documentation thoroughly
- Identify base URL and API version
- Note authentication requirements
- Check rate limits and quotas
- Review error response formats

**Plan the integration:**
- List required endpoints
- Map data models
- Identify dependencies
- Plan error handling strategy

### 2. Authentication Setup

Choose the appropriate authentication method:

**API Key:**
```python
import os

headers = {
    'X-API-Key': os.environ.get('API_KEY'),
    'Content-Type': 'application/json'
}
```

**Bearer Token:**
```python
import os

headers = {
    'Authorization': f'Bearer {os.environ.get("ACCESS_TOKEN")}',
    'Content-Type': 'application/json'
}
```

**OAuth 2.0:**
- Implement token refresh logic
- Store tokens securely
- Handle token expiration

**Basic Auth:**
```python
import os
from requests.auth import HTTPBasicAuth

username = os.environ["API_USER"]
password = os.environ["API_PASS"]
auth = HTTPBasicAuth(username, password)
```

### 3. Client Implementation

See [references/API-PATTERNS.md](references/API-PATTERNS.md) for detailed patterns.

**Basic structure:**
```python
import requests
from typing import Dict, Any

# Custom exceptions (defined here so the client below is self-contained
# when pasted alone; §4 reuses these — do not redefine them there.)
class APIError(Exception):
    """Base exception for API errors."""
    pass

class APIConnectionError(APIError):
    """Network connection failed."""
    pass

class APITimeoutError(APIError):
    """Request timed out."""
    pass

class APIAuthenticationError(APIError):
    """Authentication failed."""
    pass

class APIAuthorizationError(APIError):
    """Authorization failed (403)."""
    pass

class APINotFoundError(APIError):
    """Resource not found (404)."""
    pass

class APIRateLimitError(APIError):
    """Rate limit exceeded."""
    pass

class APIServerError(APIError):
    """Server-side error."""
    pass

class APIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        })
        self.rate_limit_remaining = None
        self.rate_limit_reset = None
    
    def _request(
        self, 
        method: str, 
        endpoint: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """Make HTTP request with error handling."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            # Track rate limits
            self.rate_limit_remaining = response.headers.get('X-RateLimit-Remaining')
            self.rate_limit_reset = response.headers.get('X-RateLimit-Reset')
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            self._handle_http_error(e)
        except requests.exceptions.ConnectionError:
            raise APIConnectionError("Failed to connect to API")
        except requests.exceptions.Timeout:
            raise APITimeoutError("Request timed out")
        except requests.exceptions.RequestException as e:
            raise APIError(f"API request failed: {str(e)}")
    
    def _handle_http_error(self, error):
        """Handle HTTP errors with specific status codes."""
        status_code = error.response.status_code
        
        if status_code == 401:
            raise APIAuthenticationError("Invalid credentials")
        elif status_code == 403:
            raise APIAuthorizationError("Insufficient permissions")
        elif status_code == 404:
            raise APINotFoundError("Resource not found")
        elif status_code == 429:
            try:
                retry_after = int(error.response.headers.get('Retry-After', 60))
            except (TypeError, ValueError):
                retry_after = 60
            e = APIRateLimitError(f"Rate limit exceeded. Retry after {retry_after}s")
            e.retry_after = retry_after
            raise e
        elif 500 <= status_code < 600:
            raise APIServerError(f"Server error: {status_code}")
        else:
            raise APIError(f"HTTP {status_code}: {error.response.text}")
```

### 4. Error Handling

**Custom exceptions:** defined at the top of the §3 client block above (APIError, APIConnectionError, APITimeoutError, APIAuthenticationError, APIAuthorizationError, APINotFoundError, APIRateLimitError, APIServerError) — the client raises them, so they must be defined before it, not here. Do not redefine them.

**Implement retry logic:**
```python
from functools import wraps
import time

def retry_on_failure(max_attempts=3, backoff_factor=2):
    """Decorator for retrying failed requests."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except APIRateLimitError as e:
                    # FIX (hackathon-ecc): the original only caught connection/server
                    # errors, so a 429 raised APIRateLimitError and never retried.
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(getattr(e, 'retry_after', 60))
                except (APIConnectionError, APIServerError):
                    if attempt == max_attempts - 1:
                        raise
                    wait_time = backoff_factor ** attempt
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator
```

### 5. Rate Limiting

**Implement rate limit handling:**
```python
import time

class RateLimiter:
    def __init__(self, calls_per_second: float):
        self.calls_per_second = calls_per_second
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0
    
    def wait_if_needed(self):
        """Wait if necessary to respect rate limit."""
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call = time.time()
```

### 6. Testing

**Test endpoints with the provided script:**
```bash
python scripts/test-endpoint.py \
    --url "https://api.example.com/v1/users" \
    --method GET \
    --headers '{"Authorization": "Bearer token"}'
```

**Write unit tests:**
```python
import pytest
import requests
from unittest.mock import Mock, patch

@pytest.fixture
def api_client():
    # Uses the §3 APIClient class defined above.
    return APIClient(base_url="https://api.example.com/v1", api_key="test-key")

def test_successful_request(api_client):
    with patch.object(api_client.session, 'request') as mock_request:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': 1, 'name': 'Test'}
        mock_request.return_value = mock_response

        result = api_client._request('GET', '/users/1')

        assert result['id'] == 1
        assert result['name'] == 'Test'

def test_rate_limit_error(api_client):
    with patch.object(api_client.session, 'request') as mock_request:
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {'Retry-After': '60'}
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_request.return_value = mock_response

        with pytest.raises(APIRateLimitError):
            api_client._request('GET', '/users/1')
```

## Best Practices

### Configuration Management
- Store API keys in environment variables
- Never commit credentials to version control
- Use different keys for dev/staging/production

### Logging
```python
# Add this method to the APIClient class above (it replaces the §3
# _request with a logging version) — it is a method, not a free function.
import logging

logger = logging.getLogger(__name__)

def _request(self, method, endpoint, **kwargs):
    url = f"{self.base_url}/{endpoint.lstrip('/')}"
    logger.info(f"API Request: {method} {endpoint}")
    try:
        response = self.session.request(method, url, **kwargs)
        logger.info(f"API Response: {response.status_code}")
        return response.json()
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        raise
```

### Response Caching
```python
# NOTE: do NOT use @lru_cache on a method — it caches per-instance (the
# instance is part of the key, so entries are never freed) and never
# expires. This version honours cache_ttl with a plain timestamped dict.
import time

class CachedAPIClient(APIClient):
    def __init__(self, *args, cache_ttl=300, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_ttl = cache_ttl
        self._user_cache = {}  # user_id -> (expires_at, result)

    def get_user(self, user_id: int):
        """Cached user lookup; entries expire after cache_ttl seconds."""
        entry = self._user_cache.get(user_id)
        if entry is not None and time.time() < entry[0]:
            return entry[1]
        result = self._request('GET', f'/users/{user_id}')
        self._user_cache[user_id] = (time.time() + self.cache_ttl, result)
        return result
```

### Pagination
```python
# Add this method to the APIClient class above — it is a method, not a
# free function.
def get_all_items(self, endpoint: str) -> list:
    """Fetch all items from paginated endpoint."""
    all_items = []
    page = 1
    
    while True:
        response = self._request('GET', endpoint, params={'page': page})
        items = response.get('data', [])
        
        if not items:
            break
            
        all_items.extend(items)
        
        if not response.get('has_more', False):
            break
            
        page += 1
    
    return all_items
```

### Webhooks
```python
import hmac
import hashlib

def verify_webhook_signature(
    payload: bytes, 
    signature: str, 
    secret: str
) -> bool:
    """Verify webhook signature."""
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected)
```

## Common Patterns

### Async/Await (Python)
```python
import aiohttp

class AsyncAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def fetch(self, endpoint: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/{endpoint}") as response:
                return await response.json()
```

### Batch Requests
```python
# Add this method to the APIClient class above — it is a method, not a
# free function.
def batch_create(self, items: list, batch_size: int = 100):
    """Create items in batches."""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        self._request('POST', '/batch', json={'items': batch})
```

## Troubleshooting

### Debug Mode
```python
import http.client
http.client.HTTPConnection.debuglevel = 1
```

### Common Issues
- **SSL Certificate errors**: Set `verify=False` temporarily (not for production!)
- **Timeout issues**: Increase timeout: `timeout=30`
- **Large responses**: Use streaming: `stream=True`
- **Rate limits**: Implement exponential backoff

## Documentation Template

Document your integration:
````markdown
# [Service Name] API Integration

## Setup
1. Get API key from [service dashboard]
2. Set environment variable: `export API_KEY=your_key`

## Usage
```python
import os
from api_client import APIClient

client = APIClient(base_url="https://api.example.com/v1", api_key=os.environ["API_KEY"])
users = client._request("GET", "/users")  # _request is the §3 client's method; there is no .get on it
```

## Rate Limits
- 1000 requests per hour
- 10 requests per second

## Error Handling
[List common errors and solutions]
````

---

Original by ihkreddy (api-integration), adapted for hackathon-ecc with functional fixes: the retry decorator catches APIRateLimitError and waits its Retry-After value (the original raised it without retrying); APIAuthorizationError and APINotFoundError are defined; the description defers named APIs to integration. Audit #3 QC fixes: the auth examples now import `os` and define their credentials; RateLimiter imports `time`; AsyncAPIClient defines `__init__` setting `base_url`; the Documentation Template imports `APIClient` (not `ServiceClient`), calls `client._request("GET", "/users")` — the method the §3 client actually defines (it has no `.get`; the `get` methods in references/API-PATTERNS.md belong to different example clients with conflicting signatures, so the template does not rely on them) — and fences its Python example properly.
