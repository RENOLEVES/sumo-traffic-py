FROM python:3.8

COPY ./requirements.txt /home
RUN pip install -r /home/requirements.txt
WORKDIR /code/server/flask_server

RUN python app.py 

WORKDIR /code


