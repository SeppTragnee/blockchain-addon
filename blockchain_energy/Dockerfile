ARG BUILD_FROM
FROM $BUILD_FROM

# Alpine Linux, gebruikt apk
RUN apk add --no-cache python3 py3-pip python3-dev build-base

# Upgrade pip en voeg wheel toe (belangrijk)
RUN pip3 install --upgrade pip wheel

# Installeer Python pakketten
RUN pip3 install requests

# Kopieer bestanden
COPY run.sh /run.sh
COPY scripts/main.py /scripts/main.py

# Geef uitvoeringsrechten
RUN chmod +x /run.sh

# Start de addon
CMD [ "/run.sh" ]
