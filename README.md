# ✨ activities

activities is a search engine for finding activities and events on Paris,
personalized with the help of a chatbot.  

## 🚀 Usage

An online demo will soon be available !

## 🔎 About

First year master's degree Natural Language Processing project.

This project uses
- 🤖 [NLTK](https://www.nltk.org/) and [spaCy](https://spacy.io/) for the chatbot
- 🌶 [Flask](https://flask.palletsprojects.com/en/2.1.x/) for both frontend and backend
- ⚡ an in-memory [Redis](https://redis.io/) database for lightning fast response times
- 📚 a [MariaDB](https://mariadb.org/) SQL database to store usage data
- 🐳 [Docker](https://www.docker.com/) and 🦄 [Gunicorn](https://gunicorn.org/) for deployment

Most of it is written in Python, with some JavaScript for the front-end, 
and some HTML / CSS for the web interface's style and structure.

## 🙌 Authors

- [Adrien Assoun](https://github.com/Arod-11)
- [Lilian Boulard](https://github.com/LilianBoulard)
- [Jary Vallimamode](https://github.com/JaryV)
- [Mohamed Ba Komara](https://github.com/komswaga)
- [Paul Jourdin](https://github.com/Paul-JD)

## 🤔 How does it work ?

Datasets are pulled from [ParisOpenData](https://opendata.paris.fr/pages/home/)
and aggregated in a normalized manner. They are then stored in a read-only
in-memory [Redis](https://redis.io/) database, which has the advantage of 
being both lightweight on the system, and extremely fast.

The search engine for filtering this data depends on the interaction between
the user and our home-brewed chatbot 🤖.  
This choice of user interface aims at shaping a friendlier and 
more comfortable interaction compared to old-fashioned forms.

## 🛠 Design

Development is centered around [Flask](https://flask.palletsprojects.com/en/2.1.x/), 
which is the web application framework we use.  
A [Redis](https://redis.io/) database is used to store the datasets, 
and a [MariaDB](https://mariadb.org/) database to record app usage.  
The chatbot is powered by [NLTK](https://www.nltk.org/) and [spaCy](https://spacy.io/) with their machine learning magic ✨

## 🔌 Self-host

### 🐳 Docker

The simplest way to run this project is to use [Docker](https://www.docker.com/),
and more specifically, [docker-compose](https://docs.docker.com/compose/).

To do that, install both, clone the repo with

```commandline
git clone https://github.com/LilianBoulard/activities
```

`cd` into it, and run

```commandline
python docker/generate_passwords.py
sudo docker-compose up -d
```

### 🐍 Directly with Python (not recommended)

If you can't use docker, you can run the project by installing 
[python](https://python.org/download) and the project's dependencies:

```commandline
pip install -r requirement.txt
```

as well as the required NLP pipelines:

```commandline
bash download_spacy_pipelines.sh
```

and finally, run `bash run_server.sh`
