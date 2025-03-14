ARG BUILD_FROM
FROM $BUILD_FROM

# Install dependencies
RUN apk add --no-cache python3 py3-pip

# Upgrade pip eerst (BELANGRIJK!)
RUN pip3 install --upgrade pip

# Install required Python packages
RUN pip3 install requests

# Copy necessary files
COPY run.sh /run.sh
COPY scripts/main.py /scripts/main.py

# Set permissions
RUN chmod +x /run.sh

# Start the addon
CMD [ "/run.sh" ]
