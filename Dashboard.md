# Setting up a Kubernetes Dashboard for monitoring in AWS EKS

### Steps:

1. Create an admin user
2. Create a service account
3. Setup clusterrole binding for the admin user
4. Get the dashboard token and the secret for accessing dashboard
5. Start kube-proxy to start the forwarding on the localhost
6. Accesss the dashboard on the web-browser 

### Sanity check on the the cluster setup

```
Venky> kubectl cluster-info

Venky> kubectl get pods


Venky> kubectl get nodes

Venky> kubectl get cs
NAME                 STATUS    MESSAGE             ERROR
controller-manager   Healthy   ok
scheduler            Healthy   ok
etcd-0               Healthy   {"health":"true"}
Venky>
```

### Setup dashboard certs, roles account

```

Venky> kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml
secret/kubernetes-dashboard-certs created
serviceaccount/kubernetes-dashboard created
role.rbac.authorization.k8s.io/kubernetes-dashboard-minimal created
rolebinding.rbac.authorization.k8s.io/kubernetes-dashboard-minimal created
deployment.apps/kubernetes-dashboard created
service/kubernetes-dashboard created
Venky>

```

### Perform service account and cluster binding

```
Venky> cat > eks-admin-service-account.yaml << EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: eks-admin
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: eks-admin
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: eks-admin
  namespace: kube-system
EOF
Venky> 


Venky> kubectl apply -f eks-admin-service-account.yaml
serviceaccount/eks-admin created
clusterrolebinding.rbac.authorization.k8s.io/eks-admin created
Venky>
```
  
  ### Get the token needed for dashboard login
  
```
Venky> kubectl get secret $(kubectl get serviceaccount dashboard -o jsonpath="{.secrets[0].name}") -o jsonpath="{.data.token}" | base64 --decode

```

### Start port forwarding

```
Venky> kubectl port-forward svc/kubernetes-dashboard -n kube-system 6443:443
Forwarding from 127.0.0.1:6443 -> 8443
Forwarding from [::1]:6443 -> 8443
Handling connection for 6443
Handling connection for 6443

```

### Access the dashboard on the localhost browser

```
https://127.0.0.1:6443/#!/login

Select 'token' option. Paste the token and click 'SIGN IN'

```

  


