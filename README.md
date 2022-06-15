# SmartCLIDE deployment service
## Prerequisites
Gitlab instance hosted repo and access token, since we use gitlab-ci to build Docker images

Running Kubernetes instance and an access bearer (see below), becouse we use a kubernetes cluster to deploy docker images from a docker registry

### Create kubernetes user and get your bearer
``` bash
# Create user
kubectl create serviceaccount k8sadmin -n kube-system
# Create role 
kubectl create clusterrolebinding k8sadmin --clusterrole=cluster-admin --serviceaccount=kube-system:k8sadmin
# Create secret
kubectl -n kube-system describe secret $(sudo kubectl -n kube-system get secret | (grep k8sadmin || echo "$_") | awk '{print $1}') | grep token: | awk '{print $2}'
# Print your token
kubectl config view | grep server | cut -f 2- -d ":" | tr -d " "
```


## Instructions for local deployment
```bash 
### Kubernetes cluster settings
export KUBE_URL='<YOUR-KUBERNETES-URL>'
export KUBE_BEARER='<YOUR-BEARER>'

# Gitlab instance settings
export GITLAB_URL='<YOUR-GITLAB-URL>'

# MOM component settings. The messages will be send to deployment-component topic of a MQTT broker
export MOM_HOST='<MOM-HOST>'
export MOM_PORT='<MOM-PORT>'
```

### Run 
``` bash 
docker-compose up -d 
```
## API documentantion 
[http://localhost:3000/docs/](http://localhost:3000/docs/)

## TODO
- Provider interface, for connecting to different Kubernetes services like AKS. Now we just connect to a bearer authenticated Kubernetes cluster
- Publish services to an accesible uri
- Integration with Kairos Interpreter
- Integration and unit tests

