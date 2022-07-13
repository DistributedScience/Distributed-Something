# Customizing Distributed-Something

Distributed-Something is a template.
It is not fully functional software but is intended to serve as an editable source so that you can quickly and easily implement a distributed workflow for your own dockerized software.

Examples of implementations can be found at [Distributed-CellProfiler](http://github.com/cellprofiler/distributed-cellprofiler), [Distributed-Fiji](http://github.com/cellprofiler/distributed-fiji), and [Distributed-OmeZarrMaker](http://github.com/cellprofiler/distributed-omezarrmaker).

There are many points at which you will need to customize Distributed-Something for your own implementation; These customization points are summarized below.
Files that do not require any customization are not listed.

## files/

### exampleFleet.json

exampleFleet.json does not need to be changed depending on your implementation of Distributed-Something.
However, each AWS account running your implementation will need to update the Fleet file with configuration specific to their account as detailed in [Step 3: Start Cluster](step_3_start_cluster.md).

### exampleJob.json

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

## worker/

### Dockerfile

The Dockerfile is used to create the Distributed-Something Docker.
You will need to edit the `FROM` to point to your own docker.

No further edits to the Dockerfile should be necessary, though advanced users make additional customizations based on the docker they are `FROM`ing.
Additionally, you may remove the section `# Install S3FS` if your workflow doesn't require mounting an S3 bucket.
You will still be able to upload and download from an S3 bucket using AWS CLI without mounting it with S3FS.

### generic-worker.py

The majority of code customization for your implementation of Distributed-Something happens in the worker file.
The `generic-worker.py` code is thoroughly documented with customization details.

### Makefile

Update `user` and `project` to match you and your Distributed-Something implementation, respectively.

### run-worker.sh

You do not need to make any modifications to run-worker.sh.
You might want to remove `2. MOUNT S3` if your workflow doesn't require mounting an S3 bucket.

## other files

### config.py

`DOCKERHUB_TAG` needs to match the `user` and `project` set in `Makefile`.
We recommend adjusting `EC2 AND ECS INFORMATION` and `DOCKER INSTANCE RUNNING ENVIRONMENT` variables to reasonable defaults for your Distributed-Something implementation.

If there are any variables you would like to pass to your program as part of configuration, you can add them at the bottom and they will be passed as system variables to the Docker.
Note that any additional variables added to `config.py` need to also be added to `CONSTANT PATHS IN THE CONTAINER` in `generic-worker.py`.

`AWS GENERAL SETTINGS` are specific to your account. All other sections are variable specific to each batch/run of your Distributed-Something implementation and will need to be adjusted at each run time. More configuration information is available in [Step 1: Configuration](step_1_configuration.md)
