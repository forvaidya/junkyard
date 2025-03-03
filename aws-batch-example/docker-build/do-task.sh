#!/bin/bash

set -x 
TSTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
OUTFILE="out_${TSTAMP}.txt"
touch $OUTFILE
pwd
readlink -f $OUTFILE
echo Arguments passed to the script: $@ >> /app/${OUTFILE}
echo ${BUCKET_NAME}
aws s3 cp /app/${OUTFILE} s3://${BUCKET_NAME}/${OUTFILE}
df -kh 







