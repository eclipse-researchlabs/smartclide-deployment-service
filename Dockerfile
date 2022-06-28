FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y python3.9-dev python3-pip libpq-dev

COPY ./src /deployment-service

WORKDIR "/deployment-service/"

RUN pip install -r requirements.txt

CMD exec /bin/bash -c "python3 deployment-service_api.py"
