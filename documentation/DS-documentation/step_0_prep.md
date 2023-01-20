# Step 0: Prep

Distributed-Something runs many parallel jobs in EC2 instances that are automatically managed by ECS.
To get jobs started, a control node to submit jobs and monitor progress is needed.
This section describes what you need in AWS and in the control node to get started.
This guide only needs to be followed once per account. 
(Though we recommend each user has their own control node, further control nodes can be created from an AMI after this guide has been followed to completion once.)

## 1. AWS Configuration

The AWS resources involved in running Distributed-Something can be primarily configured using the [AWS Web Console](https://aws.amazon.com/console/).
The architecture of Distributed-Something is based in the [worker pattern](https://aws.amazon.com/blogs/compute/better-together-amazon-ecs-and-aws-lambda/) for distributed systems.
We have adapted and simplified that architecture for Distributed-Something.

You need an active account configured to proceed. Login into your AWS account, and make sure the following list of resources is created:

### 1.1 Access keys
* Get [security credentials](http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) for your account.
Store your credentials in a safe place that you can access later.
* You will probably need an ssh key to login into your EC2 instances (control or worker nodes).
[Generate an SSH key](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) and store it in a safe place for later use.
If you'd rather, you can generate a new key pair to use for this during creation of the control node; make sure to `chmod 600` the private key when you download it.

### 1.2 Roles and permissions
* You can use your default VPC, subnet, and security groups; you should add an inbound SSH connection from your IP address to your security group.
* [Create an ecsInstanceRole](http://docs.aws.amazon.com/AmazonECS/latest/developerguide/instance_IAM_role.html) with appropriate permissions (An S3 bucket access policy CloudWatchFullAccess, CloudWatchActionEC2Access, AmazonEC2ContainerServiceforEC2Role policies, ec2.amazonaws.com as a Trusted Entity)
* [Create an aws-ec2-spot-fleet-tagging-role](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-fleet-requests.html) with appropriate permissions (just needs AmazonEC2SpotFleetTaggingRole); ensure that in the "Trust Relationships" tab it says "spotfleet.amazonaws.com" rather than "ec2.amazonaws.com" (edit this if necessary).
In the current interface, it's easiest to click "Create role", select "EC2" from the main service list, then select "EC2- Spot Fleet Tagging".

### 1.3 Auxiliary Resources
* [Create an S3 bucket](http://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html) and upload your data to it.
* Add permissions to your bucket so that [logs can be exported to it](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/S3ExportTasksConsole.html) (Step 3, first code block)
* [Create an SQS](http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/CreatingQueue.html) queue for unprocessable-messages to be dumped into (aka a DeadLetterQueue).

### 1.4 Primary Resources
The following five are the primary resources that Distributed-Something interacts with.
After you have finished preparing for Distributed-Something (this guide), you do not need to directly interact with any of these services outside of Distributed-Something.
If you would like a granular view of [what Distributed-Something is doing while it runs](overview_2.md), you can open each console in a separate tab in your browser and watch their individual behaviors, though this is not necessary, especially if you run the [monitor command](step_4_monitor.md).
* [S3 Console](https://console.aws.amazon.com/s3)
* [EC2 Console](https://console.aws.amazon.com/ec2/)
* [ECS Console](https://console.aws.amazon.com/ecs/)
* [SQS Console](https://console.aws.amazon.com/sqs/)
* [CloudWatch Console](https://console.aws.amazon.com/cloudwatch/)

### 1.5 Spot Limits
AWS initially [limits the number of spot instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-limits.html) you can use at one time; you can request more through a process in the linked documentation.
Depending on your workflow (your scale and how you group your jobs), this may not be necessary.

## 2. The Control Node
The control node can be your local machine if it is configured properly, or it can also be a small instance in AWS.
We prefer to have a small EC2 instance dedicated to controlling our Distributed-Something workflows for simplicity of access and configuration.
To login in an EC2 machine you need an ssh key that can be generated in the web console.
Each time you launch an EC2 instance you have to confirm having this key (which is a .pem file).
This machine is needed only for submitting jobs, and does not have any special computational requirements, so you can use a micro instance to run basic scripts to proceed.  

The control node needs the following tools to successfully run Distributed-Something.
Here we assume you are using the command line in a Linux machine, but you are free to try other operating systems too.

### 2.1 Make your own

#### 2.1.1 Clone this repo
You will need the scripts in Distributed-Something locally available in your control node.
<pre>
    sudo apt-get install git
    git clone https://github.com/DistributedScience/Distributed-Something.git
    cd Distributed-Something/
    git pull
</pre>

#### 2.1.2 Python 3.8 or higher and pip
Most scripts are written in Python and support Python 3.8 and 3.9.
Follow installation instructions for your platform to install python and, if needed, pip.
After Python has been installed, you need to install the requirements for Distributed-Something following this steps:

<pre>
    cd Distributed-Something/files
    sudo pip install -r requirements.txt
</pre>

#### 2.1.3 AWS CLI
The command line interface is the main mode of interaction between the local node and the resources in AWS.
You need to install [awscli](http://docs.aws.amazon.com/cli/latest/userguide/installing.html) for Distributed-Something to work properly:

<pre>
    sudo pip install awscli --ignore-installed six
    sudo pip install --upgrade awscli
    aws configure
</pre>

When running the last step, you will need to enter your AWS credentials.  
Make sure to set the region correctly (i.e. us-west-1 or eu-east-1, not eu-west-2a), and set the default file type to json.

#### 2.1.4 s3fs-fuse (optional)
[s3fs-fuse](https://github.com/s3fs-fuse/s3fs-fuse) allows you to mount your s3 bucket as a pseudo-file system.
It does not have all the performance of a real file system, but allows you to easily access all the files in your s3 bucket.
Follow the instructions at the link to mount your bucket.

#### 2.1.5 Create Control Node AMI (optional)
Once you've set up the other software (and gotten a job running, so you know everything is set up correctly), you can use Amazon's web console to set this up as an Amazon Machine Instance, or AMI, to replicate the current state of the hard drive.
Create future control nodes using this AMI so that you don't need to repeat the above installation.
