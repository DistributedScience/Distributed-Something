# Troubleshooting Your DS Implementation

## Check the Logs
Logs are automatically created in CloudWatch as a part of Distributed-Something.
If you need to troubleshoot your Distributed-Something implementation, it is likely that your error will be logged in CloudWatch.
`LOG_GROUP_NAME_perInstance` logs contain a log for every EC2 instance that is launched as a part of your Spot Fleet request and should be the first place that you look.
If your instances are successfully able to pull messages from the SQS queue, they will create a log for each job which can be easier to parse than the full `_perInstance` logs.

## AWS Credential Handling
Improper credential handling can be a blocking point in accessing many AWS services as all permissions must be explicitly granted in AWS and best practices are to set least-privilege permissions.
Distributed-Something is configured to simplify access management, but if you need to make changes to any of the recommended access management, be sure that you have carefully considered permissions.

Some of the required permissions are as follows:
run.py uses default credentials from your computer to run the following commands.
run.py doesn't pass flags to the various AWS commands so you need to have AWS CLI set up with default account having these permissions.
- `setup`: needs SQS permissions to create the queue and and ECS permissions to create the cluster and task definition.
It sends environment variables to the task definition that include either role or access keys.
If you pass a key/secret key and a role it will default to using the key/secret key for the task.
- `submitJob`: needs SQS permissions to add jobs to queue.
- `startCluster`: needs ECS permissions to create ECS config, S3 permissions to upload ECS config, EC2 permissions to launch a spot fleet, and CloudWatch permissions to create logs.

Once an EC2 instance is launched, ECS automatically puts a docker on that instance.
The fleet file determines IamFleetRole and the IamInstanceProfile. One or both of those contains permission for ECS to put the docker, and then anything that is needed in the Dockerfile (may be nothing. Could be mounting s3fs)

No AWS credentials are used to execute `Dockerfile`.

`Dockerfile` enters `run-worker.sh`.
`run-worker.sh` configures AWS CLI with environment variables.
`run-worker.sh` configures the EC2 instance and then launches workers with `generic-worker.py`.
`generic-worker.py` interacts with the SQS queue, CloudWatch, S3, and whatever else is required by your software.

If you're having a hard time with determining what credentials have been passed to your Docker, you can add `curl 169.254.170.2$AWS_CONTAINER_CREDENTIALS_RELATIVE_URI` or `aws configure list` in `run-worker.sh` to have it print the credentials that the docker is using.
