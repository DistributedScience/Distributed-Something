# Step 2: Submit Jobs

Distributed-Something works by breaking your workflow into a series of smaller jobs based on the metadata and groupings you've specified in your job file.
The choice of how to group your jobs is largely dependent on the details of your workflow.
Once you've decided on a grouping, you're ready to start configuring your job file.
Once your job file is configured, simply use `python run.py submitJob files/{YourJobFile}.json` to send all the jobs to the SQS queue [specified in your config file](step_1_configuration.md).

## Configuring your job file

All keys (outside of your groups) are shared between all jobs.

* **groups:** The list of all the groups you'd like to process.
Keys within each job can either be used to define the job (e.g. Metadata, file location) or can be used to pass job-specific variables.
For large numbers of groups, it may be helpful to create this list separately as a txt file you can then append into the jobs JSON file using your favorite scripting language.
