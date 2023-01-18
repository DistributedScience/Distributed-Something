# Introduction to Distributed-Something

Distributed-Something is a framework for scaling parallelizable jobs on [Amazon Web Services](https://aws.amazon.com/). This framework can be extended to most Dockerized tools. Distributed-Something handles the infrastructure, so that developers and end-users alike can focus on the tool and the science.

Distributed-Something is pure Python and lightweight, increasing its accessibility and usability with low-to-moderate-computational-comfort scientists.

## Distributed-Something for application developers

If the tool you want to parallelize with Distributed-Something already exists as a Docker on [Docker Hub](https://hub.docker.com/) or a repository like [BioContainers](https://biocontainers.pro/), then customization of Distributed-Something is a snap! 

Decide which aspects of the tool you wish to wrap need to be exposed to the end-user (typically: input locations, output locations, and some command line flags), and add them to the framework. Our [documentation](customization) and code comments will guide you to where things need to go. 

Add information about the customizations you added to the main [user-facing documentation](use), then share your implementation with your coworkers or the world at large!

## Distributed-Something for application users

Distributed-Something-wrapped applications endeavor to make it easy for non-computationally-comfortable end users to get started with. 

Tool users need only Python 3.7+ with `boto3` installed on the machine they wish to launch it from, and to edit plain-text files; no workflow languages required.

# Is this the only framework for scaling jobs available?

Absolutely not! We are aware of and have in many cases used the ones below. Ultimately, the right tool for your use case is the one you can get running, at a compute-cost- and human-hour-price that is optimal for you.

* [Galaxy](https://galaxyproject.org/)
* [Terra](https://terra.bio/)
* [AWS Batch](https://docs.aws.amazon.com/batch/index.html)
* [AWS Parallel Cluster](https://docs.aws.amazon.com/parallelcluster/index.html)
* [AWS Genomics CLI](https://aws.github.io/amazon-genomics-cli/docs/overview/)
