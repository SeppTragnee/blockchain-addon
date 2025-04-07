ARG BUILD_FROM
FROM ${BUILD_FROM}

# Zorg dat we bash & python en pip kunnen gebruiken
RUN apt update \
    && apt install -y bash dos2unix python3 python3-pip \
    && pip install --upgrade pip \
    && pip install requests pandas PyYAML

# Voeg je bestanden toe
COPY run.sh /run.sh
COPY scripts/ /scripts/
COPY config.yaml /config.yaml

# Maak script uitvoerbaar
RUN chmod +x /run.sh

# Start je add-on met run.sh
CMD [ "/run.sh" ]
