### Setting up a simple Helm chart.

 If you are using Helm version 3, tiller is not needed. My current version is,

```
[ec2-user@ip-10-0-0-109 templates]$ helm version
version.BuildInfo{Version:"v3.0.2", GitCommit:"19e47ee3283ae98139d98460de796c1be1e3975f", GitTreeState:"clean", GoVersion:"go1.13.5"}
[ec2-user@ip-10-0-0-109 templates]$
```

### Setup access to a repo. Lets use only stable repos.

```
[ec2-user@ip-10-0-0-109 templates]$ helm repo add stable https://kubernetes-charts.storage.googleapis.com/
"stable" has been added to your repositories
[ec2-user@ip-10-0-0-109 templates]$
```

### Searching for a stable mysql release

```
[ec2-user@ip-10-0-0-109 templates]$ helm search repo mysql

NAME                            	CHART VERSION	APP VERSION	DESCRIPTION
stable/mysql                    	1.6.2        	5.7.28     	Fast, reliable, scalable, and easy to use open-...
stable/mysqldump                	2.6.0        	2.4.1      	A Helm chart to help backup MySQL databases usi...
stable/prometheus-mysql-exporter	0.5.2        	v0.11.0    	A Helm chart for prometheus mysql exporter with...
stable/percona                  	1.2.0        	5.7.17     	free, fully compatible, enhanced, open source d...
stable/percona-xtradb-cluster   	1.0.3        	5.7.19     	free, fully compatible, enhanced, open source d...
stable/phpmyadmin               	4.2.9        	5.0.1      	phpMyAdmin is an mysql administration frontend
stable/gcloud-sqlproxy          	0.6.1        	1.11       	DEPRECATED Google Cloud SQL Proxy
stable/mariadb                  	7.3.5        	10.3.21    	Fast, reliable, scalable, and easy to use open-...

```

### To update a repo
```
[ec2-user@ip-10-0-0-109 templates]$ helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "stable" chart repository
Update Complete. ⎈ Happy Helming!⎈
[ec2-user@ip-10-0-0-109 templates]$
```

### Installing mysql pod
```
[ec2-user@ip-10-0-0-109 templates]$ helm install stable/mysql  --generate-name
NAME: mysql-1579673192
LAST DEPLOYED: Wed Jan 22 06:06:34 2020
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
MySQL can be accessed via port 3306 on the following DNS name from within your cluster:
mysql-1579673192.default.svc.cluster.local

To get your root password run:

    MYSQL_ROOT_PASSWORD=$(kubectl get secret --namespace default mysql-1579673192 -o jsonpath="{.data.mysql-root-password}" | base64 --decode; echo)

To connect to your database:

1. Run an Ubuntu pod that you can use as a client:

    kubectl run -i --tty ubuntu --image=ubuntu:16.04 --restart=Never -- bash -il

2. Install the mysql client:

    $ apt-get update && apt-get install mysql-client -y

3. Connect using the mysql cli, then provide your password:
    $ mysql -h mysql-1579673192 -p

To connect to your database directly from outside the K8s cluster:
    MYSQL_HOST=127.0.0.1
    MYSQL_PORT=3306

    # Execute the following command to route the connection:
    kubectl port-forward svc/mysql-1579673192 3306

    mysql -h ${MYSQL_HOST} -P${MYSQL_PORT} -u root -p${MYSQL_ROOT_PASSWORD}
[ec2-user@ip-10-0-0-109 templates]$
```

### Check out the pod status
```
[ec2-user@ip-10-0-0-109 templates]$ kubectl get pods -A | grep mysql
default                mysql-1579673192-56b68db6b4-52twg            1/1     Running   0          51s
[ec2-user@ip-10-0-0-109 templates]$
```

### Pods access using exposed ports
```
To access the pods using their exposed port, use  'kubectl port-forward' to have those ports
accessible to your local or another host.
```



