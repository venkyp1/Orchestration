## There are different ways secrets can be stored and used in Kubernetes cluster. Secrets are sensitive data.

### This tutorial shows a simple key-value approach for storing secrets. Secrets are stored in base64 form.

### Data:
```
username="admin"
password="sillyadmin"
secret="mysecret"
```

Store them different files.

```
echo -n $user > users.txt
echo -n $password  > password.txt
```

### Create secret

```
Venky> kubectl create secret generic $secret --from-file=./users.txt --from-file=./password.txt
secret/mysecret created
Venky> kubectl get secrets
NAME                  TYPE                                  DATA   AGE
default-token-lqwxb   kubernetes.io/service-account-token   3      80m
mysecret              Opaque                                2      8s
Venky>

Venky> kubectl describe secret $secret
Name:         mysecret
Namespace:    default
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
password.txt:  10 bytes
users.txt:     5 bytes
Venky>
```
### Get the secrets in YAML format.

```
Venky> kubectl get secrets $secret -o yaml
apiVersion: v1
data:
  password.txt: c2lsbHlhZG1pbg==
  users.txt: YWRtaW4=
kind: Secret
metadata:
  creationTimestamp: "2020-02-11T05:13:15Z"
  name: mysecret
  namespace: default
  resourceVersion: "8351"
  selfLink: /api/v1/namespaces/default/secrets/mysecret
  uid: 35537e0e-4c8d-11ea-a328-0ada6afeb9a6
type: Opaque
Venky>
```

### Decode the values to get the actual data

```
Venky> echo "c2lsbHlhZG1pbg==" | base64 --decode
sillyadmin                                                                                                         
Venky> echo "YWRtaW4=" | base64 --decode
admin
Venky>

```



