# What is going on.

## Docker file and image
To simulate a some job this docker image takes and environment variable and command line argument and output it

Sample invocation
```
docker run --rm  public.ecr.aws/z7m3o1o1/bookworm_git -- mahesh vaidya git aws 
```

## Deployment on AWS batch
Accept all defaults and refer batch-job-config.json
Since this image is built on Macbook M4, so select ARM as platform.

## You can submit job using lambda


