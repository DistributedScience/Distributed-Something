# Troubleshooting

We recommend you create a troubleshooting table that describes common failure modes for your implementation of Distributed-Something.
Shown below are errors common to most implementations of DS.
Distributed-CellProfiler documentation has a [thorough example](https://github.com/CellProfiler/Distributed-CellProfiler/wiki/Troubleshooting).

| SQS  | CloudWatch   |  S3 | EC2/ECS  | Problem  | Solution |
|---|---|---|---|---|---|
|   | Within a single log, your run command is logging multiple times. | Expected output seen. |   | A single job is being processed multiple times. | SQS_MESSAGE_VISIBILITY is set too short. See SQS-QUEUE-INFORMATION for more information. |
|   | Your specified output structure does not match the Metadata passed.  | Expected output is seen. |   | This is not necessarily an error. If the input grouping is different than the output grouping (e.g. jobs are run by Plate-Well-Site but are all output to a single Plate folder) then this will print in the CloudWatch log that matches the input structure but actual job progress will print in the CloudWatch log that matches the output structure. |   |
|   |   |   | Machines made in EC2 and dockers are made in ECS but the dockers are not placed on the machines. | There is a mismatch in your DS config file. |  Confirm that the MEMORY matches the MACHINE_TYPE  set in your config. |
