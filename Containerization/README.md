#                        Containerize your application and deploy it in Kubernetes cluster

### Overview:
  This document and repo has steps on how an application can be continerized and deployed 
in a microservices platform. Kubernetes platform is used here for the demonstration.

### Steps:


1. Creat Docker image for the application
```
     - Write a Dockerfile for the application 
     - Select and install a base OS image and tools needed
     - Assign a version
     - Dependencies - database or services needed for the application
     - Expose port(s) as needed


Venky> docker build . -t webapi:1.0 --no-cache
Sending build context to Docker daemon   25.6kB
Step 1/6 : FROM alpine
 ---> e7d92cdc71fe
Step 2/6 : RUN  mkdir /app & apk update &&       apk upgrade && apk add bash &&      apk add python && apk add py-pip &&      pip install flask
 ---> Running in c19f52b72014
fetch http://dl-cdn.alpinelinux.org/alpine/v3.11/main/x86_64/APKINDEX.tar.gz
fetch http://dl-cdn.alpinelinux.org/alpine/v3.11/community/x86_64/APKINDEX.tar.gz
v3.11.3-19-gb3a750a9f7 [http://dl-cdn.alpinelinux.org/alpine/v3.11/main]
v3.11.3-22-gaf29099ec3 [http://dl-cdn.alpinelinux.org/alpine/v3.11/community]
OK: 11258 distinct packages available
<SNIP>
Successfully installed Jinja2-2.11.0 MarkupSafe-1.1.1 Werkzeug-0.16.1 click-7.0 flask-1.1.1 itsdangerous-1.1.0
Removing intermediate container c19f52b72014
 ---> ebef4f820055
Step 3/6 : ADD  webapi.py /app
 ---> 8ee04b7a01c5
Step 4/6 : EXPOSE 5000
 ---> Running in 868c043704d8
Removing intermediate container 868c043704d8
 ---> d3d58bda7b02
Step 5/6 : WORKDIR /app
 ---> Running in f3c8280d1f8c
Removing intermediate container f3c8280d1f8c
 ---> 0bbe9d8828cc
Step 6/6 : ENTRYPOINT ["python", "/app/webapi.py"]
 ---> Running in d97d504dde95
Removing intermediate container d97d504dde95
 ---> 96542430e1eb
Successfully built 96542430e1eb
Successfully tagged webapi:1.0
Venky>

Venky> docker images | grep webapi
webapi                                                1.0                     96542430e1eb        47 seconds ago      63MB
Venky>

```


2. Aware of other docker dependencies and resources needed.
      - Should know before launching the container
      - Order of container creation may be important

3. Create a docker container and test the support locally
      - Fix issues
      - Create tests to verify the functionalities/features

```
Venky> docker run -it -p 5000:5000 webapi:1.0
 * Serving Flask app "webapi" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

```

4. This demo uses a simple python flask app and exposes a REST endpoint thru a port

```
Run few simple tests to check the API access:

Test> python3 testapi.py
test_version(): PASSED
test_negative(): PASSED
Test>

```

5. If the docker container is tested and found working as per the application requirements, push the image to a docker
   registry in DockerHub, AWS, GKE or AKS for (test/production) deployment.

   Creating a registry in AWS ECR so that this image is accessible when deployed in a Kubernetes cluster running in AWS EKS.

```
Default Region: us-east-2

Venky> aws ecr create-repository --repository-name webapi
----------------------------------------------------------------------------------
|                                CreateRepository                                |
+--------------------------------------------------------------------------------+
||                                  repository                                  ||
|+---------------------+--------------------------------------------------------+|
||  createdAt          |  1580260824.0                                          ||
||  imageTagMutability |  MUTABLE                                               ||
||  registryId         |  946775662303                                          ||
||  repositoryArn      |  arn:aws:ecr:us-east-2:946775662303:repository/webapi  ||
||  repositoryName     |  webapi                                                ||
||  repositoryUri      |  946775662303.dkr.ecr.us-east-2.amazonaws.com/webapi   ||
|+---------------------+--------------------------------------------------------+|
|||                         imageScanningConfiguration                         |||
||+---------------------------------------------+------------------------------+||
|||  scanOnPush                                 |  False                       |||
||+---------------------------------------------+------------------------------+||
Venky>

Pushing the docker image to AWS ECR:

Venky> docker tag 96542430e1eb 946775662303.dkr.ecr.us-east-2.amazonaws.com/webapi:1.0
Venky> docker push 946775662303.dkr.ecr.us-east-2.amazonaws.com/webapi:1.0
The push refers to repository [946775662303.dkr.ecr.us-east-2.amazonaws.com/webapi]
b60ec0332346: Pushed
e1890436d134: Pushed
5216338b40a7: Pushed
1.0: digest: sha256:5f0c1db8461d0b77dfa9d7dee216ab286f2896163077d365f8689a937c0fadf8 size: 947
Venky>

To check the repository:

aws ecr describe-images --repository-name webapi --region us-east-2 --output json

```
6. Create a 4 nodes Kubernetes cluster in AWS EKS

7. Write a replication manifest file for deploying the docker image in a kubernetes cluster 

```
Venky> kubectl apply -f webapi_rc.yaml
replicationcontroller/webapi-rc-deployment created
Venky>

Venky> kubectl get pods -o wide
NAME                         READY   STATUS    RESTARTS   AGE   IP               NODE                                           NOMINATED NODE   READINESS GATES
webapi-rc-deployment-65bvl   1/1     Running   0          41s   192.168.78.63    ip-192-168-89-72.us-east-2.compute.internal    <none>           <none>
webapi-rc-deployment-7df25   1/1     Running   0          41s   192.168.3.160    ip-192-168-2-151.us-east-2.compute.internal    <none>           <none>
webapi-rc-deployment-gvzk2   1/1     Running   0          41s   192.168.17.232   ip-192-168-28-118.us-east-2.compute.internal   <none>           <none>
webapi-rc-deployment-s4fq7   1/1     Running   0          41s   192.168.53.215   ip-192-168-48-145.us-east-2.compute.internal   <none>           <none>
Venky>

```

8. Access the application using supported REST endpoint to verify its working.

```

The pods are accessible only thru internal IPs, so lets run,

Venky> kubectl run curl --image=radial/busyboxplus:curl -i --tty --restart=Never
If you don't see a command prompt, try pressing enter.
[ root@curl:/ ]$
[ root@curl:/ ]$ ping 192.168.78.63
PING 192.168.78.63 (192.168.78.63): 56 data bytes
64 bytes from 192.168.78.63: seq=0 ttl=253 time=0.426 ms
64 bytes from 192.168.78.63: seq=1 ttl=253 time=0.350 ms
^C
--- 192.168.78.63 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.350/0.388/0.426 ms
[ root@curl:/ ]$ curl -s 192.168.78.63:5000/version
v1.0.0[ root@curl:/ ]$

```

9. Clean up the pods and rc

```
kubectl delete -f webapi_rc.yaml
kubectl delete pod curl
```
