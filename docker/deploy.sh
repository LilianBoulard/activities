# Install Python dependencies
pip install -r ../requirements.txt
# Download the French accurate pipeline for spaCy
python -m spacy download fr_dep_news_trf
