ARG BUILD_FROM
FROM ${BUILD_FROM}

# Make sure we can use bash & python and pip
RUN apt update \
    && apt install -y bash dos2unix python3 python3-pip \
    && pip install --upgrade pip \
    && pip install requests pandas PyYAML

# Add your files
COPY run.sh /run.sh
COPY scripts/ /scripts/
COPY config.yaml /config.yaml

# Make script executable
RUN chmod a+x /run.sh

# Start your add-on with run.sh
CMD [ "/run.sh" ]
