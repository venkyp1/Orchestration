# Container Orchestration - Kubernetes
## Using KOPS

### Overview:

  There are few popular tools available for Kubernetes setup and KOPS is one of the popular opensource tools available for that. 
   To enable access to the cluster, the setup needs a working DNS cluster. Few approaches here.
   * If you have your own domain already available for the cluster setup, use it here
   * One can use route53 in AWS to initialize DNS and use that for the cluster setup. Here is a quick setup of a small cluster in AWS. If you are using Kops 1.6.2 or later, then DNS configuration is optional. 
   * One can also use a gossip-based cluster can be easily created. The only requirement to trigger this is to have the clustername ends with .k8s.local.
   
   
  
### Requiements in AWS

```
AWS account - Create a new user 'kopsuser' for this deployment
   - Make sure to have to have FULL access for: EC2, S3, Route53, VPC, IAM
   - Verify the username:   aws iam list-users
   - Make sure the deployment zones are identified.
   - set the KOPS env variables
   
 Install awscli, kops
   - Run: aws configure
   
   ```
   
 ### Init env variables with clustername, zones  and S3 bucket. Your environment can vary.
 
 ```

      export KOPS_CLUSTER_NAME="dev.venky.com"
      export S3_BUCKET="dev-venky-com"

      # Needs a bucket for kops to store configuration files
      export KOPS_STATE_STORE="s3://${S3_BUCKET}"
      export ZONES=${MASTER_ZONES:-"us-west-1a"}
      export REGION=us-west-1
      
 ```
 
 ###  Create a S3 bucket
 
 ```

        # zone used is us-west-1. Keep it this way. It may not matter with S3
        aws s3api create-bucket --bucket ${S3_BUCKET} --region ${REGION}

        # This helps rollback the cluster if needed
        aws s3api put-bucket-versioning --bucket ${S3_BUCKET} --versioning-configuration Status=Enabled

        # aws s3 mb ${KOPS_STATE_STORE}
        # aws s3 ls
   ```
   
   #### Encrypt the S3 bucket if needed
   
```
aws s3api put-bucket-encryption --bucket ${S3_BUCKET} --server-side-encryption-configuration ‘{“Rules”:[{“ApplyServerSideEncryptionByDefault”:{“SSEAlgorithm”:”AES256"}}]}’
```

### Create the cluster

```
DRY RUN TO CHECK PARAMS:

kops create cluster \
    --cloud aws --master-size t2.medium \
    --master-count 3 \
    --master-size=t2.medium\
    --master-zones $REGION\
    --node-size=t2.medium\
    --node-count 2 \
    --zones $REGION\ \
    --ssh-public-key ./kops-aws-key.pub \
    --dry-run \
    --output json

RUN: [--yes]

kops create cluster \
    --cloud aws --master-size t2.medium \
    --master-count 3 \
    --master-size=t2.medium\
    --master-zones $REGION\
    --node-size=t2.medium\
    --node-count 2 \
    --zones $REGION\ \
    --ssh-public-key ./kops-aws-key.pub \
    --yes
    
```

### Validate the cluster

```
      kubectl config view
```

### To change configuration, 

```
kops edit cluster

Add load balancer if needed,

    spec:
  api:
    loadBalancer:
      sslCertificate: arn:aws:acm:ap-south-1:123403005789:certificate/1a2b3c54-b001–12fg-9h33-f98f7f65432d
      type: Public
  authorization:
    rbac: {}
    

```

### To save the current configuration in a YAML file

```
kops get  -o yaml > ${KOPS_CLUSTER_NAME}.yaml

```

### Access the dashboard

```

Once the cluster is started, run "kubectl proxy" to access the cluster dashboard.
The access will require a token. Run the below command to get the token for user 'admin'

kops get secrets admin --type secret -oplaintext

```

### To install PODS

```
Use: helm charts

```

### To delete the cluster [--yes is required]

```
 kops delete cluster --name ${KOPS_CLUSTER_NAME} --yes
 aws s3 rm ${KOPS_STATE_STORE}
 aws s3 ls
 
 # If route53 was configured,
    aws route53 delete-hosted-zone --id ${KOPS_CLUSTER_NAME}
```

 ### Verify
 
 ```
 kubectl cluster-info
 kubectl config view
 ```



        
      
