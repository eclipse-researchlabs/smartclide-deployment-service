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
# Create and print secret
kubectl -n kube-system describe secret $(sudo kubectl -n kube-system get secret | (grep k8sadmin || echo "$_") | awk '{print $1}') | grep token: | awk '{print $2}'
# Print k8 url
```kubectl config view | grep server | cut -f 2- -d ":" | tr -d " "```
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

<!-- eyJhbGciOiJSUzI1NiIsImtpZCI6InEtZVZFWGNiMXFESnIxSVlKQThXTTVNUUxrRFV5YnhXTUp4ZXltTTBuYm8ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJrOHNhZG1pbi10b2tlbi04OHg1diIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJrOHNhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImZlNmIzNzJlLTk0ODctNDM5ZS1hYzBlLWNiMGRmYTUzYTM3OCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTprOHNhZG1pbiJ9.d3Gg5uI9QHPeQdLefPK4hiodNiz_vgfRummwbq5QHJzJrcrYSmCiCtMCUuimLjVRKtIa6c2Y0jHIk4bdwMRn6EqfFcIBy4dno7HgT2f2JjYQgvTjP9F_IrmeSYXKirOJAwyl_nhX96XKHNqyucNuEOutWFVYabDRJIZI5V3WLBLusZCQYOLsE43I11u4MMFZJDaYEsKgi_ytVfhb-6onRDwiVBf4sWUrvXejdHSfElOh7zX7cVyMLfyrgQ9W3LzXAVJ5qg6d-7Xt1jvfthFr-5HZVHL5mBwUKMhsb-BLM-5NOckttHaFxQ3SbxSd3B_NrqNXjcfclL9WAKapvI54wrf1rui5DRgQXNZ8zc0fV75i4nkolsK_zWQt754bjmT31HwuIr0Bfu9V1IZPyYa8g1qnEHpy_S3sqUPN2fc40V37IVXA5rCBu84a6RObdNf8pxZlcNuNV8EgG6vQInwJCD-PheR09fclAsN6dBh4Qj21YcNGMPaLsgsuqgWd6SikV5tgIyD9IrVbLwKYUt-1dl8z00RwCi4YHcUh4rFJPR3u11GFz1Ql1mLqb2IWuwKHWrz9DLKg_ysZZ3_1kbuV3Pr0v-eiDZzBrV_iy_AcDmv6VnpgT_EMgn9bQB-4DATLC6EHNrIHUPR1zT_eyqjhfPpnhrJ5T8jUUAAymEktE7M -->