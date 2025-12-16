from prometheus_client import Counter, Histogram

# Count total requests
REQUEST_COUNT = Counter(
    "api_request_count",
    "Total API requests",
    ["method", "endpoint", "status"]
)

# Track latency
REQUEST_LATENCY = Histogram(
    "api_request_latency_seconds",
    "API request latency seconds",
    ["method", "endpoint"]
)
