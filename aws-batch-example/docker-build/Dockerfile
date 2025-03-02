# Use the bookworm-slim image as the base
FROM debian:bookworm-slim

# Install git, vim, aws-cli
RUN apt-get update && \
    apt-get install -y git vim awscli python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set bash as the entry point

COPY . /app
WORKDIR /app

RUN chmod a+x /app/do-task.sh


ENV BUCKET_NAME=default-bucket


ENTRYPOINT ["/bin/bash","-c","./do-task.sh $@"]







