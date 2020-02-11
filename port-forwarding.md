## This example uses a POD which exposes port 5000. This is a sample. You can use the same approach for application POD.

### Accessing a POD's port using port-forwarding

```
Venky> kubectl apply -f kube_webapi.yaml
deployment.apps/webapi-deployment created
Venky> kubectl get pods
NAME                                 READY   STATUS    RESTARTS   AGE
webapi-deployment-77799fd75f-9cwgx   1/1     Running   0          11s
webapi-deployment-77799fd75f-ssnwb   1/1     Running   0          11s
webapi-deployment-77799fd75f-zrvsd   1/1     Running   0          11s
Venky>
```

Get the exposed port:

```
Venky> kubectl describe pod webapi-deployment-77799fd75f-9cwgx | grep Port
    Port:           5000/TCP
    Host Port:      0/TCP
Venky>

```

Forward Pod's PORT to the local host:

Venky> kubectl --namespace default port-forward webapi-deployment-77799fd75f-9cwgx 5000
Forwarding from 127.0.0.1:5000 -> 5000
Forwarding from [::1]:5000 -> 5000

On another window, access the REST API from the POD:

```
Test> curl -X GET http://localhost:5000/version
v1.0.0
Test>
```



