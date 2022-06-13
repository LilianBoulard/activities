# This script is to be executed automatically inside the docker container
# when it is created.
cd /app
# Install Python dependencies
pip install -r requirements.txt
# Download the required spacy pipelines
bash ../download_spacy_pipelines.sh
# Overwrite the default config with the one made for docker
cp config.py ../activities/
# Finally, run the server
bash run_server.sh
