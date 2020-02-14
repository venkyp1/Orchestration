## Simple Swarm Cluster
### Requiements:
```
Make sure to install the following.

docker
docker-engine
docker-machine
Virtualbox (from Oracle)

```

### Initialize swarm
```
Venky>  docker swarm init                                                                             
Swarm initialized: current node (t92xx8ps2ljj65vzcesbcnhva) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-2b45iz9olvcr2nfsm0tzjmyfhb65cqhbrs3uq43qspp2usc2v8-6fhaqumdnie22s11qfq1pqva9 192.168.65.3:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.

Venky> 

Venky>  docker info                                                                                     
Client:
 Debug Mode: false

Server:
 Containers: 35
  Running: 2
  Paused: 0
  Stopped: 33
 Images: 17
 Server Version: 19.03.4
 Storage Driver: overlay2
  Backing Filesystem: extfs
  Supports d_type: true
  Native Overlay Diff: true
 Logging Driver: json-file
 Cgroup Driver: cgroupfs
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null o
<SNIP>
```

### Check node

```

Venky>  docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS      ENGINE VERSION
t92xx8ps2ljj65vzcesbcnhva *   docker-desktop      Ready               Active              Leader              19.03.4
Venky>
```
### Create 3 worker nodes

```
docker-machine create --driver virtualbox <worker-node-name>

Check them using:

docker-machine ls

```

### SSH into each node and join them to docker swarm
```
Venky> docker-machine ssh worker1     #<<<==== use name
   ( '>')
  /) TC (\   Core is distributed with ABSOLUTELY NO WARRANTY.
 (/-_--_-\)           www.tinycorelinux.net

docker@worker1:~$ docker swarm join --token SWMTKN-1-2s042pgxprx8ncfyuixbo1z9d8zrp4d1shr27wa6n4uad6dob6-42uazh2p2dhm79wb4k9nozqkz 192.168.99.102:2377
This node joined a swarm as a worker.
docker@worker1:~$
```
Now the swarm is ready for container deployment.

#### Note: Update the docker-compose.yml 'apiVersion' to '3'

### Deploy Stack
```
Venky> docker stack deploy --compose-file docker-compose.yml myswarm               
Creating network myswarm_default
Creating service myswarm_jenkins
Venky>

Venky> docker stack services myswarm                                             
ID                  NAME                MODE                REPLICAS            IMAGE                        PORTS
jv2y02ziuw3x        myswarm_jenkins     replicated          0/1                 jenkinsci/blueocean:latest   *:8080->8080/tcp, *:8443->8443/tcp, *:50000->50000/tcp
Venky>
```

### To bring down the swarm cluster:
```
Venky> docker stack rm myswarm

To leave the swarm :

  This will take your node out of swarm.

Venky> docker swarm leave --force
```

### Some useful commands:

```
To change the status of a node(worker/manager):

   docker node update --help

   docker node update --availability ["active"|"pause"|"drain"]  NODE

   docker node update --role ["worker"|"manager"]   NODE    # worker TO manager vice versa.

To scale the number of containers:

   docker service scale myspark=5   [myspark is a docker image. This will run 5 myspark containers.]
   
To start myspark container with 2 replicas:

   docker service create --replicas 2 -p 7077:7077 -p 8080:8080 --name myspark venky/myspark
```
   
