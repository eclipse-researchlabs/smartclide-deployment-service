# SmartCLIDE deployment component
## Prerequisites
Gitlab instance hosted repo and access token, since we use gitlab-ci for contructing Docker images

Running Kubernetes instance and an access bearer (see below), becouse we use kubernetes cluster to deploy docker images from a docker registry

### Create kubernetes user and get your bearer
``` bash
kubectl create serviceaccount k8sadmin -n kube-system
kubectl create clusterrolebinding k8sadmin --clusterrole=cluster-admin --serviceaccount=kube-system:k8sadmin
kubectl -n kube-system describe secret $(sudo kubectl -n kube-system get secret | (grep k8sadmin || echo "$_") | awk '{print $1}') | grep token: | awk '{print $2}'
kubectl config view | grep server | cut -f 2- -d ":" | tr -d " "
```

## Instrucctions for local deployment
### Kubernetes cluster settings
```bash 
export KUBE_URL='<YOUR-KUBERNETES-URL>'
export KUBE_BEARER='<YOUR-BEARER>'
```
### Gitlab instance settings
```bash 
export GITLAB_URL='<YOUR-GITLAB-URL>'
```
### Run 
``` bash 
docker-compose up -d 
```
### API documentantion 
```bash
http://localhost:3000/docs/