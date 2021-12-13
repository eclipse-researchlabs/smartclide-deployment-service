FROM ubuntu:20.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y python3.6 \
    python3.9-dev python3-pip libpq-dev
COPY . /deployment_component
WORKDIR "/deployment_component/src"
RUN pip install -r requirements.txt
# CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
# ENV KUBERNETES_SERVICE_HOST=192.168.39.21
# ENV KUBERNETES_SERVICE_PORT=8443
ENV KUBECONFIG=/etc/kubernetes/admin.conf
CMD exec /bin/bash -c "python3 deployment-service_api.py"

# CMD ["python deployment-service_api.py"]