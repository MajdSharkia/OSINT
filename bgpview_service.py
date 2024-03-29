# bgpview_service.py

from flask import Flask, request, jsonify
import requests
import redis
import json
from datetime import datetime, timedelta
import osint_common

app = Flask(__name__)
cache = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

# Flush the cache
cache.flushall()

BGP_VIEW_BASE_URL = "https://api.bgpview.io/ip/"

@app.route('/bgp_view_service', methods=['GET'])
def get_bgp_view_service():
    start_time = datetime.now()
    ip_address = request.args.get('ip')
    # Check cache first
    cached_response = osint_common.get_cached_response(cache, ip_address)
    if cached_response:
        print("bgp_view_service: {} found in cache".format(ip_address))
        data = cached_response
    else:
        print("bgp_view_service: {} not found in cache".format(ip_address))
        bgp_view_response = requests.get(f"{BGP_VIEW_BASE_URL}{ip_address}")
        data = {}
        if bgp_view_response:
            data = bgp_view_response.json()
        data["status_code"] = bgp_view_response.status_code
        # Cache the response
        osint_common.cache_response(cache, ip_address, data)
    
    end_time = datetime.now()
    elapsed_time = (end_time - start_time).total_seconds()
    
    # Prepare response JSON
    response_data = {
            "time": str(elapsed_time),
            "data": data
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)


