ARG BUILD_FROM
FROM ${BUILD_FROM}

#instalem python, pip i llibreries que necessitarem
RUN apt update \
    && apt install -y dos2unix python3 python3-pip \
    && pip install --upgrade pip \

# Kopieer bestanden naar container
COPY run.sh /run.sh
COPY scripts /scripts
COPY config.yaml /config.yaml

# Permissies instellen
RUN chmod +x /run.sh

# Start add-on
CMD [ "/run.sh" ]
