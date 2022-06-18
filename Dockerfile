FROM python:3.10 AS intermediate

RUN apt-get update -y
RUN apt-get install -y git git-lfs

WORKDIR /usr/src/app
COPY . .

# Install Python dependencies
RUN pip install --upgrade --disable-pip-version-check --no-input -r requirements.txt
# Download the required spacy pipelines
RUN sh download_pretrained_models.sh

# Expose the required port(s)
EXPOSE 8000

# Launch the server at runtime
ENTRYPOINT ["sh", "run_server.sh"]
