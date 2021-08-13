FROM osgeo/gdal:ubuntu-small-latest

# Install python/pip
RUN apt -y install python3.8-distutils && \
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.8 get-pip.py

COPY requirements.txt /home/
RUN pip install --requirement /home/requirements.txt


# SUMO installation
ENV SUMO_HOME=/usr/share/sumo

RUN apt-get -y update; apt-get -y install software-properties-common; add-apt-repository ppa:sumo/stable
RUN apt-get -y update; apt-get -y install sumo sumo-tools sumo-doc

# setting bash dir
WORKDIR /home














# ARG V_BASE=3.3.0

# FROM opendatacube/geobase-builder:${V_BASE} as env_builder
# COPY requirements.txt /tmp
# COPY constraints.txt /tmp
# RUN env-build-tool new /tmp/requirements.txt /tmp/constraints.txt /env

# FROM opendatacube/geobase-runner:${V_BASE}
# COPY --from=env_builder /env /env
# ENV LC_ALL=C.UTF-8
# ENV PATH="/env/bin:${PATH}"

# COPY requirements.txt /home/
# RUN pip install --requirement /home/requirements.txt



# # Install sumo system dependencies
# RUN apt-get update && apt-get -qq install \
#     wget \
#     g++ \
#     make \
#     libfox-1.6-0 libfox-1.6-dev \
#     unzip

# # solve a problem with shared library missing for sumo (xerces-c-3.1)
# WORKDIR /home
# RUN wget http://archive.apache.org/dist/xerces/c/3/sources/xerces-c-3.1.4.zip \
#     && unzip xerces-c-3.1.4.zip \
#     && cd xerces-c-3.1.4 \
#     && ./configure \
#     && make \
#     && make install \
#     && export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib