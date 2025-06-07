FROM python:3.10-slim

# Install Redis
RUN apt-get update && apt-get install -y redis-server && apt-get clean

# Set working directory
WORKDIR /app

# Copy your app code
COPY . .

# Install Python dependencies
RUN pip install redis alpaca-py

# Run both Redis and the publisher script in one CMD
CMD bash -c "redis-server --daemonize yes && python Pub.py"
