FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y python3-pip git curl

COPY ./src /deployment-service
WORKDIR "/deployment-service/"
RUN curl https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz -o ./geckodriver
ENV PYTHONPATH=/deployment-service/
RUN pip install -r requirements.txt

CMD exec /bin/bash -c "python3 deployment-service_api.py"
# CMD sleep infinity