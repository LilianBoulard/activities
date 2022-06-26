# ✨ activities

activities is a search engine for finding activities and events on Paris,
personalized with the help of a chatbot.  

## 🚀 Usage

An online demo is available here: http://app.boulard.fr:8000/

## 🔎 About

First year master's degree Natural Language Processing project.

This project uses
- 🤖 [spaCy](https://spacy.io/) for the chatbot
- 🌶 [Flask](https://flask.palletsprojects.com/en/2.1.x/) for both frontend and backend
- ⚡ an in-memory [Redis](https://redis.io/) database for lightning fast response times
- 📚 a [MariaDB](https://mariadb.org/) SQL database to store usage data
- 🐳 [Docker](https://www.docker.com/) and 🦄 [Gunicorn](https://gunicorn.org/) for deployment

Most of it is written in Python, with some JavaScript for the front-end, 
and some HTML / CSS for the web interface's style and structure.

## 🙌 Authors

- [Lilian Boulard](https://github.com/LilianBoulard) - Lead
- [Adrien Assoun](https://github.com/Arod-11) - NLP & processes
- [Jary Vallimamode](https://github.com/JaryV) - NLP
- [Mohamed Ba Komara](https://github.com/komswaga) - DB & UI
- [Paul Jourdin](https://github.com/Paul-JD) - NLP & UI

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
The chatbot is powered by [spaCy](https://spacy.io/) magic ✨

### 🤔 Design choices

#### Why Redis ?

Datasets wrote in Redis at runtime are afterwards read-only, 
therefore we don't care about the ACID properties of the database.  
Furthermore, Redis is known to be extremely fast, which is a plus !

#### Why spaCy ?

spaCy provides pretrained French pipelines, which avoids us doing the tedious
training part 😄  
We tried using [Rasa](https://rasa.com/open-source/) and 
[🤗 CamemBERT](https://huggingface.co/Jean-Baptiste/camembert-ner-with-dates)
but in the end it didn't fit our processes and what we wanted to do !

#### Why Docker ?

'cause deploying an entire service with essentially one command is cool 😎  
*(and other techy reasons, but [who cares about that](docker/README.md) 😴)*

## 🔌 Self-host

### 🐳 Docker

The simplest (and currently only) way to run this project is to use 
[Docker](https://www.docker.com/), and more specifically, 
[docker-compose](https://docs.docker.com/compose/).

To do that, install both, then clone the repo with

```commandline
git clone https://github.com/LilianBoulard/activities
```

`cd` into it, and run

```commandline
python docker/generate_passwords.py
sudo docker-compose up -d
```

and you should be good to go !

If you need more information on this process, check out [our documentation](docker/README.md)
