FROM alpine:latest

# Install apache bench and other utilities
RUN apk add --no-cache apache2-utils curl bash

# Create a script directory
WORKDIR /scripts

# Copy the load test script
COPY loadtest.sh /scripts/loadtest.sh

# Make the script executable
RUN chmod +x /scripts/loadtest.sh

# Run the load test script
CMD ["/scripts/loadtest.sh"]
