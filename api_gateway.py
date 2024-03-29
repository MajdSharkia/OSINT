# api_gateway.py

import asyncio
import ipaddress
from datetime import datetime
import aiohttp
from flask import Flask, request, jsonify

app = Flask(__name__)

#from quart import Quart, request, jsonify
#app = Quart(__name__)

# Define the base URL of the IP-API.com microservice
IP_API_SERVICE_URL = 'http://localhost:5000/ip_api_service'
BGP_VIEW_SERVICE_URL = 'http://localhost:5001/bgp_view_service'

class OSINTCollector:
    def __init__(self):
        self.total_time = 0
        self.global_status = "success"
        self.response_data = {
            "metrics": {
                "ip-api": {},
                "bgview": {}
            },
            "raw_data": {
                "ip-api": {},
                "bgview": {}
            }
        }

    def validate_ip_list(self, ip_list):
        """
        Validate if a string is a comma-separated list of IP addresses.
        :param ip_list: str, a string of IP addresses separated by commas
        :return: bool, True if the input string is a valid IP list, False otherwise
        """
        if not ip_list:
            return False
        ip_list = ip_list.split(',')
        for ip_address in ip_list:
            ip_address = ip_address.strip()
            try:
                ipaddress.ip_address(ip_address)
            except ValueError:
                return False
        return True
    
    async def fetch_data(self, url, ip_address):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}?ip={ip_address}")as response:
                return await response.json()

    def parse_data(self, ip_address, api_response, service):
            status = "fail"
            if api_response['data']['status_code'] == 200: # Check if the connection in succeeded
                status = api_response['data']['status']
                status = status.replace("ok", "success") # In BGP it's returns ok instead of success

            time_taken = float(api_response['time'])
            self.response_data["metrics"][service][ip_address] = {
                "status": status,
                "time": time_taken
            }

            # Update metrics for global total
            self.total_time += time_taken
            # Update total success/fail - We assume that success means that all requests passed, fail - at least one failed.
            if status != "success":
                self.global_status = status

            # Add raw data for each IP address
            self.response_data["raw_data"][service][ip_address] = api_response['data']

    async def collect_data(self, ip_addresses_list):
        
        # Fetch data for each IP address concurrently from both services
        ip_api_tasks = [self.fetch_data(IP_API_SERVICE_URL, ip_address) for ip_address in ip_addresses_list]
        bgp_view_tasks = [self.fetch_data(BGP_VIEW_SERVICE_URL, ip_address) for ip_address in ip_addresses_list]

        ip_api_responses = await asyncio.gather(*ip_api_tasks)
        bgp_view_responses = await asyncio.gather(*bgp_view_tasks)

        # We can imporove the loop by running it in parallel, but then we need to take care of the shard variable total_time and global_status by using a lock
        for ip_address, ip_api_response, bgp_view_response in zip(ip_addresses_list, ip_api_responses, bgp_view_responses):
            self.parse_data(ip_address, ip_api_response, "ip-api")
            self.parse_data(ip_address, bgp_view_response, "bgview")
        
        # Update global status and total_time in the response
        self.response_data["metrics"]["total"] = {
            "status": self.global_status,
            "time": self.total_time
        }
        return self.response_data
     
@app.route('/<path:ip_addresses>', methods=['GET'])
async def osint(ip_addresses):
    start_time = datetime.now()
    print(f"osint: Received request for IP addresses: {ip_addresses}")
    
    # Extract IP addresses from the URL path)
    osint_collector = OSINTCollector()
    if not osint_collector.validate_ip_list(ip_addresses):
        return jsonify({'error': "Invalid Input"})
    ip_addresses_list = ip_addresses.split(',')
    response_data = await osint_collector.collect_data(ip_addresses_list)
    end_time = datetime.now()
    elapsed_time = (end_time - start_time).total_seconds()
    print("osint: Elapsed_time = {}".format(elapsed_time))
    response_data["metrics"]["total"]["api-time"] = elapsed_time
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

