# ip_api_service.py

from flask import Flask, request, jsonify
import requests
import redis
from datetime import datetime
import osint_common

app = Flask(__name__)
cache = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Flush the cache
cache.flushall()

IP_API_BASE_URL = "http://ip-api.com/json/"


@app.route('/ip_api_service', methods=['GET'])
def get_ip_api_service():
    start_time = datetime.now()
    ip_address = request.args.get('ip')
    # Check cache first
    cached_response = osint_common.get_cached_response(cache, ip_address)
    if cached_response:
        print("ip_api_service: {} found in cache".format(ip_address))
        data = cached_response
    else:
        print("ip_api_service: {} not found in cache".format(ip_address))
        ip_api_response = requests.get(f"{IP_API_BASE_URL}{ip_address}")
        data = ip_api_response.json()
        data["status_code"] = ip_api_response.status_code
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
    app.run(host='0.0.0.0', port=5000)


