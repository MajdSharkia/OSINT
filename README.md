# OSINT

A containerized system for performing basic OSINT on given IP addresses.
Here's a high-level overview of the system architecture:
* Containerization: We'll containerize the system using Docker for easy deployment
* Microservices Architecture: The system will consist of multiple microservices, each responsible for fetching data from a specific API. This architecture allows for modularity and scalability.
* API Gateway: An API Gateway will handle incoming HTTP requests and distribute them to the appropriate microservices.
* Caching: We'll implement caching to store responses from the last hour, reducing response time for frequently queried IP addresses.
* Performance: The system will be designed to support multiple concurrent requests efficiently.


Components:

    API Gateway:
        Exposes an HTTP API that receives IP addresses as input.
        Routes requests to appropriate microservices.
        Aggregates responses from microservices and returns a single response to the client.

    Microservices:
        ip-api-service:
            Fetches geolocation data from the IP-API.com API.
        bgpview-service:
            Fetches data from the BGPView API.
        Each microservice:
            Receives IP address(es) from the API Gateway.
            Fetches data from the corresponding external API.
            Returns the response to the API Gateway.

    Caching:
        Utilize a caching mechanism (Redis) to store responses from the last hour.
        Before making a request to an external API, check if the response is cached. If so, return the cached response.

    Performance:
        Implement asynchronous request handling in microservices to support multiple concurrent requests efficiently.
        Use appropriate concurrency mechanisms and optimizations to minimize response times.

Technologies:

    Docker: Containerization.
    Flask: API Gateway and microservices.
    Redis: Caching.
    Python requests library: Making HTTP requests to external APIs.

Deployment:
    Clone the repository containing the source code.
    Deploy the Docker containers using DockerFile.
    Expose the API Gateway to the internet to receive incoming requests.

Example Request:

http

GET http://localhost/176.228.193.161

Response:

{"metrics": {

    "bgview": {
      "176.228.193.161": {
        "status": "success",
        "time": 0.928473
      }
    },
    "ip-api": {
      "176.228.193.161": {
        "status": "success",
        "time": 0.258012
      }
    },
    "total": {
      "api-time": 1.669995,
      "status": "success",
      "time": 1.186485
    }
    },"raw_data": {
    "bgview": {
      "176.228.193.161": {
        "@meta": {
          "api_version": 1,
          "execution_time": "65.29 ms",
          "time_zone": "UTC"
        },
        "data": {
          "iana_assignment": {
            "assignment_status": "allocated",
            "date_assigned": null,
            "description": "RIPE NCC",
            "whois_server": "whois.ripe.net"
          },
          "ip": "176.228.193.161",
          "maxmind": {
            "city": null,
            "country_code": null
          },
          "prefixes": [
            {
              "asn": {
                "asn": 12400,
                "country_code": "IL",
                "description": "Partner Communications Ltd.",
                "name": "PARTNER-AS"
              },
              "cidr": 17,
              "country_code": "IL",
              "description": null,
              "ip": "176.228.128.0",
              "name": null,
              "prefix": "176.228.128.0/17"
            },
            {
              "asn": {
                "asn": 12400,
                "country_code": "IL",
                "description": "Partner Communications Ltd.",
                "name": "PARTNER-AS"
              },
              "cidr": 14,
              "country_code": "IL",
              "description": null,
              "ip": "176.228.0.0",
              "name": null,
              "prefix": "176.228.0.0/14"
            }
          ],
          "ptr_record": "176-228-193-161.orange.net.il",
          "rir_allocation": {
            "allocation_status": "allocated",
            "cidr": 14,
            "country_code": null,
            "date_allocated": "2011-12-01 00:00:00",
            "ip": "176.228.0.0",
            "prefix": "176.228.0.0/14",
            "rir_name": "RIPE"
          }
        },
        "status": "ok",
        "status_code": 200,
        "status_message": "Query was successful"
      }
    },
    "ip-api": {
      "176.228.193.161": {
        "as": "AS12400 Partner Communications Ltd.",
        "city": "Rishon LeTsiyyon",
        "country": "Israel",
        "countryCode": "IL",
        "isp": "Partner Communications",
        "lat": 31.9642,
        "lon": 34.7876,
        "org": "",
        "query": "176.228.193.161",
        "region": "M",
        "regionName": "Central District",
        "status": "success",
        "status_code": 200,
        "timezone": "Asia/Jerusalem",
        "zip": ""
      }
    }
  }
  }
