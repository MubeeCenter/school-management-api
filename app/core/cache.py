import redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def get_cache(key: str):
    data = r.get(key)
    if data:
        return json.loads(data)
    return None

def set_cache(key: str, value, ttl: int = 300):
    r.set(key, json.dumps(value), ex=ttl)

def delete_cache(key: str):
    r.delete(key)
