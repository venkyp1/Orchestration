## Horizontal autoscale - Demo
 
### Overview: 
```
  Horizontal pods autoscaling is a resource management feature. Based on the need of a resource (CPU, Memory),
this allows to scale the number of running PODS. For example, when more CPU resource is needed, more PODs can 
be scheduled and whenthe CPU consumptions falls below a preset limit, the PODS can be scaled down by terminating excess PODs.
```

### Requirements

```
1. Create a docker container in ECR using the given Dockerfile
2. Make changes to the autopod_deploy.yaml file as needed for deployment
3. Setup HPA
```

### Setup
```
Venky> kubectl create -f autopod_deploy.yaml
deployment.apps/autopod-deployment created
Venky> kubectl autoscale deployment autopod-deployment --cpu-percent=10 --min=1 --max=3
horizontalpodautoscaler.autoscaling/autopod-deployment autoscaled
Venky> 

Venky> kubectl get pods
NAME                                  READY   STATUS    RESTARTS   AGE
autopod-deployment-7667f85745-7k77m   1/1     Running   0          47s
Venky> 

Venky> kubectl get hpa
NAME                 REFERENCE                       TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
autopod-deployment   Deployment/autopod-deployment   1%/10%    1         3         1          10m
Venky> 

There is only one POD running and HPA is configured for up to THREE pods if needed.

```

## Test HPA

```
 Once the initial setup is done, let's login to the running POD and run the below script at bash.
      /app/make_cpu_busy.sh 10000 &

 All it does is generating 10000 random numbers. This will start putting stress on the CPU and increase its load go past
the limit set. At that time, HPA will kick in to create additional POD(s). You can run the command again on the new
POD also, to make sure HPA reached the number of PODs limit.

Venky> kubectl get hpa
NAME                 REFERENCE                       TARGETS    MINPODS   MAXPODS   REPLICAS   AGE
autopod-deployment   Deployment/autopod-deployment   167%/10%   1         3         1          15m
➜  autoscale_pods kubectl get pods
Venky> 

Watch New PODs were created.

Venky> kubectl get pods
NAME                                  READY   STATUS    RESTARTS   AGE
autopod-deployment-7667f85745-7k77m   1/1     Running   0          15m
autopod-deployment-7667f85745-fjhxr   1/1     Running   0          8s
autopod-deployment-7667f85745-vmzs2   1/1     Running   0          8s
Venky> 

Venky> kubectl get hpa
NAME                 REFERENCE                       TARGETS    MINPODS   MAXPODS   REPLICAS   AGE
autopod-deployment   Deployment/autopod-deployment   167%/10%   1         3         3          16m
Venky> 


When the random generator stopped, the CPU usages died down and so the excess PODS.
Venky>
kubectl get pods
NAME                                  READY   STATUS    RESTARTS   AGE
autopod-deployment-7667f85745-7k77m   1/1     Running   0          52m
metrics-server-57b898595c-vpl5w       1/1     Running   0          138m
Venky> 
```

### Delete deployment and PODS
```
Venky> kubectl delete hpa autopod-deployment
horizontalpodautoscaler.autoscaling "autopod-deployment" deleted
Venky> kubectl delete -f autopod_deploy.yaml
deployment.apps "autopod-deployment" deleted
Venky> 

Make sure to delete the repo in ECR also.
```





