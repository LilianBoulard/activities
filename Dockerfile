FROM python:3.9 AS build

RUN apk add --no-cache git

WORKDIR /usr/src/app
COPY . ./

# Install Python dependencies
RUN pip install -r requirements.txt
# Download the required spacy pipelines
RUN bash download_spacy_pipelines.sh

# Overwrite the default config with the one made for docker
RUN cp docker/config.py activities/

# Flatten to single layer image
FROM scratch
COPY --from=build /app /app
ENTRYPOINT ["/app"]
# Run the server at runtime
CMD ["bash", "run_server.sh"]
