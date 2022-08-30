# Step 3: Start Cluster

After your jobs have been submitted to the queue, it is time to start your cluster.
Once you have configured your spot fleet request per the instructions below, you may run
`python run.py startCluster files/{YourFleetFile}.json`

When you enter this command, the following things will happen (in this order):

* Your spot fleet request will be sent to AWS.
Depending on their capacity and the price that you bid, it can take anywhere from a couple of minutes to several hours for your machines to be ready.
* Distributed-Something will create the APP_NAMESpotFleetRequestId.json file, which will allow you to [start your progress monitor](step_4_monitor.md).
This will allow you to walk away and just let things run even if your spot fleet won't be ready for some time.

Once the spot fleet is ready:

* Distributed-Something will create the log groups (if they don't already exist) for your log streams to go in.
* Distributed-Something will ask AWS to place Docker containers onto the instances in your spot fleet.
Your job will begin shortly!

***
## Configuring your spot fleet request
Definition of many of these terms and explanations of many of the individual configuration parameters of spot fleets are covered in AWS documentation [here](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-fleet.html) and [here](http://docs.aws.amazon.com/cli/latest/reference/ec2/request-spot-fleet.html).
You may also configure your spot fleet request through Amazon's web interface and simply download the JSON file at the "review" page to generate the configuration file you want, though we do not recommend this as Distributed-Something assumes a certain fleet request structure and has only been tested on certain Amazon AMI's.
Looking at the output of this automatically generated spot fleet request can be useful though for obtaining values like your VPC's subnet and security groups, as well the ARN ID's of your roles.

Among the parameters you should/must update:

* **The IamFleetRole, IamInstanceProfile, KeyName, SubnetId, and Groups:** These are account specific and you will configure these based on the [previous setup work that you did](step_0_prep.md).
Once you've created your first complete spot fleet request, you can save a copy as a local template so that you don't have to look these up every time.

  * The KeyName used here should be the same used in your config file but **without** the `.pem` extension.

* **ImageId and SnapshotId** These refer to the OS and pre-installed programming that will be used by your spot fleet instances, and are both AWS region specific.
We use the Amazon ECS-Optimized Amazon Linux AMI; but the Linux 2 AMI also seems to work in our limited testing.
If there is no template fleet file for your region, or the one here is too out-of-date, see below for instructions on configuring these options yourselves.
If you have a good working configuration for a region that isn't represented or for a more up-to-date version of the AMI than we've had time to test, please feel free to create a pull request and we'll include it in the repo!

## To run in a region where a spot fleet config isn't available or is out of date:

* Under EC2 -> Instances select "Launch Instance"

![Launch Instance](images/Launch.jpg)

* Search "ECS", then choose the "Amazon ECS-Optimized Amazon Linux AMI"

![Select ECS-Optimized](images/ECS.jpg)

* Select Continue, then select any instance type (we're going to kill this after a few seconds) and click "Next: Configure Instance Details"

* Choose a network and subnet in the region you wish to launch instances in, and then click "Next: Add Storage"

![Set Network and Subnet](images/Network.jpg)

* On the "Add Storage" page, note down the Snapshot column for the Root volume- this is your SnapshotId.
Click "Review and Launch"

![Get SnapshotId](images/Snapshot.jpg)

* Click "Launch", and then select any key pair (again, we'll be killing this in a few seconds)

* Once your instance has launched, click its link from the launch page.

![Click InstanceID](images/InstanceID.jpg)

* In the list of information on the instance, find and note its AMI ID - this is your ImageId

![Get the AMI ID](images/AMIID.jpg)

* Terminate the instance
