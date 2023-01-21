# What is Distributed-Something?

Distributed-Something is a series of scripts designed to help you run a Dockerized version of your software on [Amazon Web Services](https://aws.amazon.com/) (AWS) using AWS's file storage and cloud computing systems.

Distributed-Something:
* simplifies the process of distributing and running software in the cloud.
* decreases the cost of cloud computing by optimizing resources used.
* makes workflows reproducible.
* is Python based which makes creating new implementations broadly accessible to intermediate computationalists.
* only requires human-readable configuration to run an implementation which makes it broadly accessible to novice computationalists.

You will need to customize Distributed-Something for your particular use case.
See [Customizing Distributed-Something](customizing_DS.md) for customization details.

## What is Docker?

Docker is a software platform that packages software into containers.
In a container is the software that you want to run as well as everything needed to run it (e.g. your software source code, operating system libraries, and dependencies).

Dockerizing a workflow has many benefits including
* Ease of use: Dockerized software doesn't require the user to install anything themselves.
* Reproducibility: You don't need to worry about results being affected by the version of your software or its dependencies being used as those are fixed.

## Why would I want to use this?

Using AWS allows you to create a flexible, on-demand computing infrastructure where you only have to pay for the resources you use.
This can give you access to far more computing power than you may have available at your home institution, which is great when you have large datasets to process.
However, typically each piece of the infrastructure has to be added and configured separately, which can be time-consuming and confusing.

Distributed-Something tries to leverage the power of the former, while minimizing the problems of the latter.

## What do I need to have to run this?

Essentially all you need to run Distributed-Something is an AWS account and a terminal program; see our [page on getting set up](step_0_prep.md) for all the specific steps you'll need to take.
You will also need a Dockerized version of your software.

## Can I contribute code to Distributed-Something?

Feel free!  We're always looking for ways to improve.

## Who made this?

Distributed-Something is a project from the [Cimini Lab](https://cimini-lab.broadinstitute.org) in the Imaging Platform at the Broad Institute in Cambridge, MA, USA.
It was initially conceived and implemented for a single use case as [Distributed-CellProfiler](https://github.com/CellProfiler/Distributed-CellProfiler) in what is now the [Carpenter-Singh Lab](https://carpenter-singh-lab.broadinstitute.org).
