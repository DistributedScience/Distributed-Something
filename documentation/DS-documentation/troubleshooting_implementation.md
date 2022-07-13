# Troubleshooting Your Distributed-Something Implementation

## Check the Logs

## AWS Credential Handling
run.py uses default credentials from computer to run following commands.
run.py doesn't pass flags to the various AWS commands so you need to have AWS CLI set up with default account having these permissions.
- setup: needs SQS permissions to create queue and and ECS permissions to create cluster and task definition.
Sends environment variables to task definition that include either role or access keys.
- submitJob: needs SQS permissions to add jobs to queue.
- startCluster: needs ECS permissions to create ECS config, S3 permissions to upload ECS config, EC2 permissions to launch a spot fleet, Cloudwatch permissions to create logs.

Once an EC2 instance is launched, ECS automatically puts a docker on that instance.
Fleet file determines IamFleetRole and the IamInstanceProfile. One or both of those contains permission for ECS to put the docker, and then anything that is needed in the Dockerfile (may be nothing. Could be mounting s3fs)
Dockerfile is executed. No AWS credentials are used in this step.

Dockerfile enters run-worker.sh.
run-worker.sh configures AWS CLI with environment variables.
run-worker.sh configures the EC2 instance and then launches workers with generic-worker.py.
generic-worker.py runs


If you're having a hard time with credentials, you can pass `curl 169.254.170.2$AWS_CONTAINER_CREDENTIALS_RELATIVE_URI` in run-worker.sh to show the credentials that the docker is using. or `aws configure list`

If you pass a key/secret key and a role it will default to key/secret key to task.
