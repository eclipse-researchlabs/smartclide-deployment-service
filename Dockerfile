FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y python3-pip git wget

COPY ./src /deployment-service
WORKDIR "/deployment-service/"
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz 
RUN tar -xvf geckodriver-v0.31.0-linux64.tar.gz && rm geckodriver-v0.64.0-linux32.tar.gz

ENV PATH=/deployment-service/
RUN pip install -r requirements.txt

CMD exec /bin/bash -c "python3 deployment-service_api.py"
# CMD sleep infinity