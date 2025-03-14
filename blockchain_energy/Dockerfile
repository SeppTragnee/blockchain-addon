ARG BUILD_FROM
FROM ${BUILD_FROM}

# Installeer Python en pip
RUN apt update && apt install -y python3 python3-pip

# Installeer Python-pakketten (één voor één om problemen te isoleren)
RUN pip3 install requests
RUN pip3 install pandas
RUN pip3 install scikit-learn
RUN pip3 install psutil
RUN pip3 install numpy
RUN pip3 install holidays
RUN pip3 install tomli
RUN pip3 install func_timeout

# Voeg bestanden toe
ADD ./rootfs/server.py /server.py
ADD ./rootfs/bottle.py /bottle.py
ADD ./rootfs/sqlDB.py /sqlDB.py
COPY ./rootfs/www/www/ /www/
COPY ./rootfs/images/ /images/
COPY ./rootfs/optimalScheduler/ /optimalScheduler/

# Kopieer configuratiebestand
COPY config.yaml /config.yaml

# Kopieer en geef uitvoeringsrechten aan het startscript
COPY ./rootfs/run.sh /run.sh
RUN chmod a+x /run.sh

# Start de add-on
CMD ["/run.sh"]
