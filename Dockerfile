# Use the official Ubuntu image as the base image
FROM ubuntu:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    redis \
    redis-server \
    # Add any other dependencies you need here
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy your Python files into the container
COPY api_gateway.py /app/api_gateway.py
COPY ip_api_service.py /app/ip_api_service.py
COPY bgpview_service.py /app/bgpview_service.py
COPY osint_common.py /app/osint_common.py
COPY start_services.sh /app/start_services.sh


# Add any other files you need here

# Install Python dependencies
RUN pip3 install flask httpx redis quart requests aiohttp flask[async]

# Expose the port your Flask app runs on
EXPOSE 80

# Command to run your application
#CMD ["/bin/bash"]
#CMD ["./start_services.sh"]
