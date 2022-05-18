# ✨ activities

activities is a search engine for finding activities and events on Paris,
personalized with the help of a chatbot.  

An online demo will soon be available !

## 🔎 About

First year master's degree Natural Language Processing project.

This project uses
- 🤖 [NLTK](https://www.nltk.org/) for the chatbot
- 🌶 [Flask](https://flask.palletsprojects.com/en/2.1.x/) for both frontend and backend
- ⚡ an in-memory [Redis](https://redis.io/) database for lightning fast response times
- 📚 a [MariaDB](https://mariadb.org/) SQL database to store usage data
- 🐳 [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) for deployment

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
and are aggregated in a normalized manner. They are then stored in a read-only
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
The chatbot is powered by [NLTK](https://www.nltk.org/) with its machine learning magic ✨

## 🔌 Usage

The simplest way to run this project is to use [Docker](https://www.docker.com/),
and more specifically, [docker-compose](https://docs.docker.com/compose/).

To do that, install both and run

```commandline
sudo docker-compose up -d
```
