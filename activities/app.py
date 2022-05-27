import pandas as pd
from .database.sql import db
from .database.sql.models import Event

import dateutil
from sqlalchemy.orm import sessionmaker
from flask import Blueprint, render_template, jsonify, request

app = Blueprint('main', __name__)
Session = sessionmaker(bind=db)


def populate_db():
    df = pd.read_csv('doc/que-faire-a-paris-.csv', delimiter=';')
    with Session() as session:
        for i, line in df.iterrows():
            lon, lat = map(float, line['Coordonnées géographiques'].split(','))
            session.add(Event(
                title=line['Titre'],
                tags=line['Mots clés'],
                date_start=dateutil.parser.isoparse(line['Date de début']),
                longitude=lon,
                latitude=lat,
            ))
        session.commit()


def describe_db():
    with Session() as session:
        res = session.query(Event)
        print(type(res), len(res))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/nltkresponse', methods=['POST'])
def nltkresponse():
    #user_message = request.form['data']
    #print(user_message)
    results = {'message': "C'est noté !"}
    return jsonify(results)


populate_db()
describe_db()
