# SmartiCLIDE deployment component

### Create kuberbetes user and get your bearer
``` bash
kubectl create serviceaccount k8sadmin -n kube-system
kubectl create clusterrolebinding k8sadmin --clusterrole=cluster-admin --serviceaccount=kube-system:k8sadmin
kubectl -n kube-system describe secret $(sudo kubectl -n kube-system get secret | (grep k8sadmin || echo "$_") | awk '{print $1}') | grep token: | awk '{print $2}'
kubectl config view | grep server | cut -f 2- -d ":" | tr -d " "
```