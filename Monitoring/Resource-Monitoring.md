# Kubernets cluster resource monitoring using Metrics-server.

### Note: Heapster has been deprected. So this demo uses metrics-server for monitoring.

### Requirements
```
Kubernetes Cluster
helm [Version: 3]
Pods running [Using CPU and Memory, so monitoring the resources make sense :-) ]
```


## Verify requirements
```
Venky> kubectl get nodes
NAME                                           STATUS   ROLES    AGE    VERSION
ip-192-168-12-48.us-east-2.compute.internal    Ready    <none>   164m   v1.14.7-eks-1861c5
ip-192-168-21-151.us-east-2.compute.internal   Ready    <none>   164m   v1.14.7-eks-1861c5
ip-192-168-48-229.us-east-2.compute.internal   Ready    <none>   164m   v1.14.7-eks-1861c5
ip-192-168-72-29.us-east-2.compute.internal    Ready    <none>   164m   v1.14.7-eks-1861c5
Venky> helm version --short
v3.0.2+g19e47ee
Venky> kubectl version --short
Client Version: v1.14.8
Server Version: v1.14.9-eks-c0eccc
Venky>

Venky> kubectl create -f nginx_deploy.yaml

```

## Search and Install metrics-server in a new namespace(monitoring)

```
Search for a stable version:

Venky> helm search repo metrics-server
NAME                 	CHART VERSION	APP VERSION	DESCRIPTION
stable/metrics-server	2.9.0        	0.3.6      	Metrics Server is a cluster-wide aggregator of ...
Venky>

Create monitoring namespace:

Venky> kubectl create namespace monitoring
namespace/monitoring created
Venky>

Before deploying the metrics-server, make changes to its manifest file.

Venky> helm show values stable/metrics-server > metrics-server.values

Make the following changes in the file:

Enable the host network:

hostNetwork:
  # Specifies if metrics-server should be started in hostNetwork mode.
  #
  # You would require this enabled if you use alternate overlay networking for pods and
  # API server unable to communicate with metrics-server. As an example, this is required
  # if you use Weave network on EKS
  enabled: true

Add insecure TLS access as shown below:

args:
- --kubelet-insecure-tls

Save and close the file.

Venky> helm install  metrics-server stable/metrics-server --namespace monitoring --values metrics-server.values
NAME: metrics-server
LAST DEPLOYED: Thu Feb 13 19:32:27 2020
NAMESPACE: monitoring
STATUS: deployed
REVISION: 1
NOTES:
The metric server has been deployed.

In a few minutes you should be able to list metrics using the following
command:

  kubectl get --raw "/apis/metrics.k8s.io/v1beta1/nodes"
Venky>

```

## Make sure the metrics-server is started and no errors
```
Venky> kubectl logs -n monitoring metrics-server-57b898595c-qbpdd
I0214 03:32:32.489440       1 serving.go:312] Generated self-signed cert (/tmp/apiserver.crt, /tmp/apiserver.key)
I0214 03:32:33.544173       1 secure_serving.go:116] Serving securely on [::]:8443
Venky>
```

## Verify all pods

```
Venky> kubectl -n monitoring get all
NAME                                  READY   STATUS    RESTARTS   AGE
pod/metrics-server-57b898595c-qbpdd   1/1     Running   0          97s

NAME                     TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/metrics-server   ClusterIP   10.100.39.37   <none>        443/TCP   97s

NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/metrics-server   1/1     1            1           97s

NAME                                        DESIRED   CURRENT   READY   AGE
replicaset.apps/metrics-server-57b898595c   1         1         1       97s
Venky> kubectl get pods
NAME                               READY   STATUS    RESTARTS   AGE
nginx-deployment-6dd86d77d-pt4j4   1/1     Running   0          45m
nginx-deployment-6dd86d77d-wqcpf   1/1     Running   0          45m
Venky> kubectl get pods -n monitoring
NAME                              READY   STATUS    RESTARTS   AGE
metrics-server-57b898595c-qbpdd   1/1     Running   0          2m6s
Venky> 
```

## Time to verify the metrics-server stats

```
Venky> kubectl top nodes
NAME                                           CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
ip-192-168-12-48.us-east-2.compute.internal    22m          2%     289Mi           32%
ip-192-168-21-151.us-east-2.compute.internal   26m          2%     285Mi           32%
ip-192-168-48-229.us-east-2.compute.internal   23m          2%     370Mi           41%
ip-192-168-72-29.us-east-2.compute.internal    23m          2%     232Mi           26%
Venky> kubectl -n kube-system top pods
NAME                       CPU(cores)   MEMORY(bytes)
aws-node-jcdt7             1m           21Mi
aws-node-k8mw7             2m           10Mi
aws-node-v5sh4             1m           22Mi
aws-node-v9jgz             2m           10Mi
coredns-74dd858ddc-pnb6n   2m           7Mi
coredns-74dd858ddc-zcbz2   2m           7Mi
kube-proxy-475hc           2m           9Mi
kube-proxy-bqfcb           2m           7Mi
kube-proxy-kbf7z           3m           8Mi
kube-proxy-t5dmp           1m           7Mi
Venky>

```

## JSON output 

```
Venky> kubectl get --raw "/apis/metrics.k8s.io/v1beta1/nodes" | jq .
{
  "kind": "NodeMetricsList",
  "apiVersion": "metrics.k8s.io/v1beta1",
  "metadata": {
    "selfLink": "/apis/metrics.k8s.io/v1beta1/nodes"
  },
  "items": [
    {
      "metadata": {
        "name": "ip-192-168-12-48.us-east-2.compute.internal",
        "selfLink": "/apis/metrics.k8s.io/v1beta1/nodes/ip-192-168-12-48.us-east-2.compute.internal",
        "creationTimestamp": "2020-02-14T03:52:46Z"
      },
      "timestamp": "2020-02-14T03:52:23Z",
      "window": "30s",
      "usage": {
        "cpu": "19631235n",
        "memory": "296864Ki"
      }
    },
    {
      "metadata": {
        "name": "ip-192-168-21-151.us-east-2.compute.internal",
        "selfLink": "/apis/metrics.k8s.io/v1beta1/nodes/ip-192-168-21-151.us-east-2.compute.internal",
        "creationTimestamp": "2020-02-14T03:52:46Z"
      },
      "timestamp": "2020-02-14T03:52:24Z",
      "window": "30s",
      "usage": {
        "cpu": "23450096n",
        "memory": "282120Ki"
      }
    },
    {
      "metadata": {
        "name": "ip-192-168-72-29.us-east-2.compute.internal",
        "selfLink": "/apis/metrics.k8s.io/v1beta1/nodes/ip-192-168-72-29.us-east-2.compute.internal",
        "creationTimestamp": "2020-02-14T03:52:46Z"
      },
      "timestamp": "2020-02-14T03:52:26Z",
      "window": "30s",
      "usage": {
        "cpu": "23126644n",
        "memory": "238232Ki"
      }
    },
    {
      "metadata": {
        "name": "ip-192-168-48-229.us-east-2.compute.internal",
        "selfLink": "/apis/metrics.k8s.io/v1beta1/nodes/ip-192-168-48-229.us-east-2.compute.internal",
        "creationTimestamp": "2020-02-14T03:52:46Z"
      },
      "timestamp": "2020-02-14T03:52:24Z",
      "window": "30s",
      "usage": {
        "cpu": "20044284n",
        "memory": "379476Ki"
      }
    }
  ]
}
Venky>
```


#### THAT'S ALL





