import json
from datetime import timedelta

def get_cached_response(cache, ip_address):
    cached_data = cache.get(ip_address)
    if cached_data:
        return json.loads(cached_data)
    return None

def cache_response(cache, ip_address, response):
    cache.setex(ip_address, timedelta(hours=1), json.dumps(response))

