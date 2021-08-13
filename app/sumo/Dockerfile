FROM ubuntu:bionic

ENV SUMO_HOME=/usr/share/sumo

RUN apt-get -y update; apt-get -y install software-properties-common; add-apt-repository ppa:sumo/stable
RUN apt-get -y update; apt-get -y install sumo sumo-tools sumo-doc
# RUN cp -f /usr/bin/sumo /usr/share/sumo/bin
# RUN cp -f /usr/bin/sumo-gui /usr/share/sumo/bin