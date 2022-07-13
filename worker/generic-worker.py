import boto3
import json
import logging
import os
import subprocess
import time
import watchtower

#################################
# CONSTANT PATHS IN THE CONTAINER
#################################

DATA_ROOT = "/home/ubuntu/bucket"
LOCAL_OUTPUT = "/home/ubuntu/local_output"
QUEUE_URL = os.environ["SQS_QUEUE_URL"]
AWS_BUCKET = os.environ["AWS_BUCKET"]
LOG_GROUP_NAME = os.environ["LOG_GROUP_NAME"]
CHECK_IF_DONE_BOOL = os.environ["CHECK_IF_DONE_BOOL"]
EXPECTED_NUMBER_FILES = os.environ["EXPECTED_NUMBER_FILES"]
if "MIN_FILE_SIZE_BYTES" not in os.environ:
    MIN_FILE_SIZE_BYTES = 1
else:
    MIN_FILE_SIZE_BYTES = int(os.environ["MIN_FILE_SIZE_BYTES"])
if "USE_PLUGINS" not in os.environ:
    USE_PLUGINS = "False"
else:
    USE_PLUGINS = os.environ["USE_PLUGINS"]
if "NECESSARY_STRING" not in os.environ:
    NECESSARY_STRING = False
else:
    NECESSARY_STRING = os.environ["NECESSARY_STRING"]
if "DOWNLOAD_FILES" not in os.environ:
    DOWNLOAD_FILES = False
else:
    DOWNLOAD_FILES = os.environ["DOWNLOAD_FILES"]
# If you added more system variables to config.py, enter them here

localIn = "/home/ubuntu/local_input"


#################################
# CLASS TO HANDLE THE SQS QUEUE
#################################


class JobQueue:
    def __init__(self, queueURL):
        self.client = boto3.client("sqs")
        self.queueURL = queueURL

    def readMessage(self):
        response = self.client.receive_message(
            QueueUrl=self.queueURL, WaitTimeSeconds=20
        )
        if "Messages" in response.keys():
            data = json.loads(response["Messages"][0]["Body"])
            handle = response["Messages"][0]["ReceiptHandle"]
            return data, handle
        else:
            return None, None

    def deleteMessage(self, handle):
        self.client.delete_message(QueueUrl=self.queueURL, ReceiptHandle=handle)
        return

    def returnMessage(self, handle):
        self.client.change_message_visibility(
            QueueUrl=self.queueURL, ReceiptHandle=handle, VisibilityTimeout=60
        )
        return


#################################
# AUXILIARY FUNCTIONS
#################################


def monitorAndLog(process, logger):
    while True:
        output = process.stdout.readline().decode()
        if output == "" and process.poll() is not None:
            break
        if output:
            print(output.strip())
            logger.info(output)


def printandlog(text, logger):
    print(text)
    logger.info(text)


#################################
# RUN SOME PROCESS
#################################


def runSomething(message):
    # List the directories in the bucket- this prevents a strange S3Fs error
    # You can remove this if you are not mounting S3FS
    rootlist = os.listdir(DATA_ROOT)
    for eachSubDir in rootlist:
        subDirName = os.path.join(DATA_ROOT, eachSubDir)
        if os.path.isdir(subDirName):
            trashvar = os.system("ls " + subDirName)

    # Configure the logs
    logger = logging.getLogger(__name__)

    # Parse your message to pull out a name variable to use for logging
    # To include all group keys in your log name, use the commented-out code below
    # Otherwise, create your own definition of metadataID
    # group_to_run = message["group"]
    # groupkeys = list(group_to_run.keys())
    # groupkeys.sort()
    # metadataID = '-'.join(groupkeys)

    # Add a handler with
    watchtowerlogger = watchtower.CloudWatchLogHandler(
        log_group=LOG_GROUP_NAME, stream_name=str(metadataID), create_log_group=False
    )
    logger.addHandler(watchtowerlogger)

    # See if this is a message you've already handled, if you've so chosen
    # First, build a variable called remoteOut that equals your unique prefix of where your output should be
    # e.g remoteOut = os.path.join(message['output'], metadataID)

    # Then check if there are too many files
    if CHECK_IF_DONE_BOOL.upper() == "TRUE":
        try:
            s3client = boto3.client("s3")
            bucketlist = s3client.list_objects(
                Bucket=AWS_BUCKET, Prefix=remoteOut + "/"
            )
            objectsizelist = [k["Size"] for k in bucketlist["Contents"]]
            objectsizelist = [i for i in objectsizelist if i >= MIN_FILE_SIZE_BYTES]
            if NECESSARY_STRING:
                if NECESSARY_STRING != "":
                    objectsizelist = [
                        i for i in objectsizelist if NECESSARY_STRING in i
                    ]
            if len(objectsizelist) >= int(EXPECTED_NUMBER_FILES):
                printandlog("File not run due to > expected number of files", logger)
                logger.removeHandler(watchtowerlogger)
                return "SUCCESS"
        except KeyError:  # Returned if that folder does not exist
            pass

    # If you need to download files locally, perform that step here
    # printandlog("Downloading files", logger)

    # Build and run your program's command
    # e.g. cmd = my-program --my-flag-1 True --my-flag-2 VARIABLE

    # Assign the variable "localOut" to the output location where you expect your program to put files
    # e.g. localOut = os.path.join(LOCAL_OUTPUT, metadataID)

    print("Running", cmd)
    logger.info(cmd)
    subp = subprocess.Popen(
        cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    monitorAndLog(subp, logger)

    # Figure out a done condition - a number of files being created, a particular file/folder being created, an exit code, etc.
    # Set its success to the boolean variable `done`
    # e.g. done = os.path.isfile(os.path.join(localOut, program.is.done))

    # Get the outputs and move them to S3
    if done:
        time.sleep(30)
        mvtries = 0
        while mvtries < 3:
            try:
                printandlog("Move attempt #" + str(mvtries + 1), logger)
                cmd = (
                    "aws s3 mv "
                    + localOut
                    + " s3://"
                    + AWS_BUCKET
                    + "/"
                    + remoteOut
                    + " --recursive"
                )
                subp = subprocess.Popen(
                    cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                out, err = subp.communicate()
                out = out.decode()
                err = err.decode()
                printandlog("== OUT \n" + out, logger)
                if err == "":
                    break
                else:
                    printandlog("== ERR \n" + err, logger)
                    mvtries += 1
            except:
                printandlog("Move failed", logger)
                printandlog("== ERR \n" + err, logger)
                time.sleep(30)
                mvtries += 1
        if mvtries < 3:
            printandlog("SUCCESS", logger)
            logger.removeHandler(watchtowerlogger)
            return "SUCCESS"
        else:
            printandlog(
                "SYNC PROBLEM. Giving up on trying to sync " + metadataID, logger
            )
            import shutil

            shutil.rmtree(localOut, ignore_errors=True)
            logger.removeHandler(watchtowerlogger)
            return "PROBLEM"
    else:
        printandlog("PROBLEM: Failed exit condition for " + metadataID, logger)
        logger.removeHandler(watchtowerlogger)
        import shutil

        shutil.rmtree(localOut, ignore_errors=True)
        return "PROBLEM"


#################################
# MAIN WORKER LOOP
#################################


def main():
    queue = JobQueue(QUEUE_URL)
    # Main loop. Keep reading messages while they are available in SQS
    while True:
        msg, handle = queue.readMessage()
        if msg is not None:
            result = runSomething(msg)
            if result == "SUCCESS":
                print("Batch completed successfully.")
                queue.deleteMessage(handle)
            else:
                print("Returning message to the queue.")
                queue.returnMessage(handle)
        else:
            print("No messages in the queue")
            break


#################################
# MODULE ENTRY POINT
#################################

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Worker started")
    main()
    print("Worker finished")
