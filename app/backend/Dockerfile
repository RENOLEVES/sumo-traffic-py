FROM osgeo/gdal:ubuntu-small-latest

# Install python/pip
RUN apt -y install python3.8-distutils && \
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.8 get-pip.py


# SUMO installation
ENV SUMO_HOME=/usr/share/sumo

RUN apt-get -y update; apt-get -y install software-properties-common; add-apt-repository ppa:sumo/stable
RUN apt-get -y update; apt-get -y install sumo sumo-tools sumo-doc

# setting bash dir
COPY requirements.txt /home/requirements.txt
WORKDIR /home
RUN pip install -r requirements.txt
