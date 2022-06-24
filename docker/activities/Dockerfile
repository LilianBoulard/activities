FROM python:3.9 AS intermediate

WORKDIR /usr/src/app

RUN apt-get update -qq
RUN apt-get update -y
RUN apt-get install -y git
RUN rm -rf /var/cache/apt

# Make a copy of the code at the time of build.
# This directory will be updated with a git pull at runtime.
COPY . .

# Install Python dependencies
RUN pip install --upgrade --disable-pip-version-check --no-input -r requirements.txt
# Download the required spacy pipelines
RUN sh download_pretrained_models.sh

# Expose the required port(s)
EXPOSE 8000

# Launch the server at runtime
ENTRYPOINT ["sh", "run_server.sh"]
