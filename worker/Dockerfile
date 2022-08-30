#
#                                 - [ BROAD'16 ] -
#
# A docker instance for accessing AWS resources
# This wraps the cellprofiler docker registry
#


FROM someuser/somedocker:sometag

# Install S3FS 

RUN apt-get -y update           && \
    apt-get -y upgrade          && \
    apt-get -y install 		\
	automake 		\
	autotools-dev 		\
	g++ 			\
	git 			\
	libcurl4-gnutls-dev 	\
	libfuse-dev 		\
	libssl-dev 		\
	libxml2-dev 		\
	make pkg-config		\
	sysstat			\
	curl

WORKDIR /usr/local/src
RUN git clone https://github.com/s3fs-fuse/s3fs-fuse.git
WORKDIR /usr/local/src/s3fs-fuse
RUN ./autogen.sh
RUN ./configure
RUN make
RUN make install

# Install Python - not needed if you've already got it in your container
# If you have a non-3.8 version, you will need to change python3.8 calls where specified

RUN apt install -y python3.8-dev python3.8-distutils

# Install AWS CLI

RUN python3.8 -m pip install awscli 

# Install boto3

RUN python3.8 -m pip install boto3

# Install watchtower for logging

RUN python3.8 -m pip install watchtower

# SETUP NEW ENTRYPOINT

RUN mkdir -p /home/ubuntu/
WORKDIR /home/ubuntu
COPY generic-worker.py .
COPY instance-monitor.py .
COPY run-worker.sh .
RUN chmod 755 run-worker.sh

WORKDIR /home/ubuntu
ENTRYPOINT ["./run-worker.sh"]
CMD [""]

