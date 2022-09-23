# Customizing DS

Distributed-Something is a template.
It is not fully functional software but is intended to serve as an editable source so that you can quickly and easily implement a distributed workflow for your own Dockerized software.

Examples of implementations can be found at [Distributed-CellProfiler](http://github.com/cellprofiler/distributed-cellprofiler), [Distributed-Fiji](http://github.com/cellprofiler/distributed-fiji), and [Distributed-OmeZarrMaker](http://github.com/cellprofiler/distributed-omezarrmaker).

## Customization overview

Before starting to customize Distributed-Something code, do some research on your desired implementation.

1) Ask how splittable is the function you want to distribute?
If the end product you envision cannot easily be split into small tasks then it may not be a good fit for Distributed-Something.
2) Make or find a Docker of the software you want to distribute.
You can find over 1000 scientific softwares already Dockerized at [Biocontainers](http://biocontainers.pro) and many open-source softwares provide Docker files within their GitHub repositories.
See [Implementing Distributed-Something](implementing_DS.md) for more details.
3) Figure out how to make your software run from the command line.
What parameters do you need to pass to it?
What is generic to how you like to run the application and what is different for each job?

## Customization details

There are many points at which you will need to customize Distributed-Something for your own implementation; These customization points are summarized below.
Files that do not require any customization are not listed.

### files/

#### exampleFleet.json

exampleFleet.json does not need to be changed depending on your implementation of Distributed-Something.
However, each AWS account running your implementation will need to update the Fleet file with configuration specific to their account as detailed in [Step 3: Start Cluster](step_3_start_cluster.md).

#### exampleJob.json

exampleJob.json needs to be entirely customized for your implementation of Distributed-Something.
When you submit your jobs in [Step 2: Submit Jobs](step_2_submit_jobs.md), Distributed-Something adds a job to your SQS queue for each item in `groups`.
Each job contains the shared variables common to all jobs, listed in the exampleJob.json above the `groups` key.
These variables are passed to your worker as the `message` and should include any metadata that may possibly change between runs of your Distributed-Something implementation.  

Some common variables used in Job files include:
- input location
- output location
- output structure
- script/pipeline name
- flags to pass to your program

### worker/

#### Dockerfile

The Dockerfile is used to create the Distributed-Something Docker.
You will need to edit the `FROM` to point to your own docker.

No further edits to the Dockerfile should be necessary, though advanced users make additional customizations based on the docker they are `FROM`ing.
Additionally, you may remove the section `# Install S3FS` if your workflow doesn't require mounting an S3 bucket.
You will still be able to upload and download from an S3 bucket using AWS CLI without mounting it with S3FS.

#### generic-worker.py

The majority of code customization for your implementation of Distributed-Something happens in the worker file.
It is responsible for parsing the input message, creating the call command, and figuring out how to determine if your task succeeded or failed.
The `generic-worker.py` code is thoroughly documented with customization details.

#### Makefile

Update `user` and `project` to match you and your Distributed-Something implementation, respectively.
Decide on a `tag` to use.
Note that you an use `latest` for the `tag` while your are developing/testing your software (it will continually overwrite) and give it a numbered tag when you have a functional version.

#### run-worker.sh

You do not need to make any modifications to run-worker.sh.
You might want to remove `2. MOUNT S3` if your workflow doesn't require mounting an S3 bucket.
If you change the name of the generic-worker.py , and/or if you plan to change the Python versions, reflect those changes here.

### other files

#### config.py

`DOCKERHUB_TAG` needs to match the `user` and `project` set in `Makefile`.
We recommend adjusting `EC2 AND ECS INFORMATION` and `DOCKER INSTANCE RUNNING ENVIRONMENT` variables to reasonable defaults for your Distributed-Something implementation.
Suggestions for determining optimal parameters can be found in [Implementing Distributed-Something](implementing_DS.md).

If there are any variables you would like to pass to your program as part of configuration, you can add them at the bottom and they will be passed as system variables to the Docker.
Note that any additional variables added to `config.py` need to also be added to `CONSTANT PATHS IN THE CONTAINER` in `generic-worker.py`.

`AWS GENERAL SETTINGS` are specific to your account. All other sections are variable specific to each batch/run of your Distributed-Something implementation and will need to be adjusted at each run time.
More configuration information is available in [Step 1: Configuration](step_1_configuration.md)

#### run.py

If you have changed anything in config.py, you will need to edit the section on Task Definitions to match.
