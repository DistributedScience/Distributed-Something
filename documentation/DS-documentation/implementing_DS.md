# Implementing your Distributed-Something

## Make your software docker

## Make your Distributed-Something docker

How to make a docker:
do this stuff
`make`
Note that you can set :latest in makefile and in config.py

## Test requirements for config.py

To test necessary parameters:
Create Ec2 instance.
Use AMI with S3FS already installed
setup cloudwatch agent for more comprehensive usage stats (https://docs.google.com/document/d/1Gi8eHRmvTrQUdBO2aUjby_bzW5iUV68xcSIm_NPUhPo/edit)
install docker with `sudo apt install docker.io`
`sudo docker run -it --rm --entrypoint /bin/sh -v ~/bucket:/bucket DOCKER`
