#!/bin/bash

/usr/bin/redis-server &
python3 api_gateway.py &
python3 ip_api_service.py &
python3 bgpview_service.py &
