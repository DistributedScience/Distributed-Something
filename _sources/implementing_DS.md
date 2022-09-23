# Implementing DS

## Make your software Docker

Your software will need to be containerized in its own Docker.
This Docker image is what you will `FROM` in `Dockerfile` when you create your Distributed-Something Docker image.
Detailed instructions are out of the scope of this documentation, though we refer you to [Docker's documentation](https://docs.docker.com/get-started/).
For examples that we use in our Distributed-Something suite, you can refer to the code used to make the [CellProfiler Docker](https://github.com/CellProfiler/distribution/tree/master/docker), [BioFormats2Raw Docker](https://github.com/ome/bioformats2raw-docker), and [Fiji Docker](https://github.com/fiji/dockerfiles).

## Make your Distributed-Something Docker

Once you have made all the alterations to the Distributed-Something code detailed in [Customizing Distributed-Something](customizing_DS.md), you need to make your Distributed-Something Docker image.

You will need a [DockerHub account](https://hub.docker.com).
Connect to the Docker daemon.
We find the simplest way to do this is to download and open Docker Desktop.
You can leave Docker Desktop open in the background while you continue to work at the command line.

<pre>
# Navigate into the Distributed-Something/worker folder
cd worker
# Run the make command
make
</pre>

While it is generally a good principle to iterate numerical tags, note that you can set the tag to `latest` in both `Makefile` and in `config.py` to simplify troubleshooting (as you don't have to remember to change the tag in either location while potentially testing multiple Docker builds).

## Test requirements for config.py

Once you have created a functional Docker image of your software, it is useful to know exact memory requirements so you can request appropriately sized machines in `config.py`.
We recommend using CloudWatch Agent on an AWS instance.
(Standard CloudWatch metrics do not report granular memory usage.)

To test necessary parameters:
- Create a EC2 instance using an AMI with S3FS already installed.
- Add an IAM role. This machine must have an instance role with sufficient permissions attached in order to transmit metrics.
- Connect to your EC2 instance.
- Install CloudWatch Agent following [AWS documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/download-cloudwatch-agent-commandline.html).

<pre>
# Start CloudWatch Agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json
# Install Docker
sudo apt install docker.io
# Run
sudo docker run -it --rm --entrypoint /bin/sh -v ~/bucket:/bucket DOCKER
# Stop CloudWatch Agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -m ec2 -a stop
</pre>

View your collected memory metrics in CloudWatch:
- CloudWatch => Metrics => All Metrics
- Custom Namespaces => CWAgent => ImageId, InstanceId, InstanceType => YOUR_INSTANCE mem_used_percent
- Graphed metrics => PERIOD = 1 Minute (or whatever you have set in your CloudWatch config)
