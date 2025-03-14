ARG BUILD_FROM
FROM $BUILD_FROM

# Basisinstallatie python en pip
RUN apk add --no-cache python3 py3-pip

# Installeer/upgrade pip + wheel (vereist!)
RUN pip3 install --upgrade pip wheel

# Installeer alleen requests (meer heb je momenteel niet nodig)
RUN pip3 install requests

# Kopieer bestanden naar container
COPY run.sh /run.sh
COPY scripts /scripts
COPY config.yaml /config.yaml

# Permissies instellen
RUN chmod +x /run.sh

# Start add-on
CMD [ "/run.sh" ]
