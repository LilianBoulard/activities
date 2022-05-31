import pandas as pd
from .database.sql import db
from .database.sql.models import Event

import dateutil
from flask import Blueprint, render_template, jsonify, request

app = Blueprint('app', __name__)


@app.route('/newEvent', methods=['GET'])
def populate_db():
    # Remove old events
    db.session.query(Event).delete()
    db.session.commit()
    # Add new ones
    df = pd.read_csv('doc/que-faire-a-paris-.csv', delimiter=';')
    # Only keep important columns
    df = df[['Titre', 'Coordonnées géographiques', 'Mots clés', 'Date de début']]
    # Remove lines with missing values
    df = df.dropna()
    for i, line in df.iterrows():
        lon, lat = map(float, line['Coordonnées géographiques'].split(','))
        db.session.add(Event(
            title_event=line['Titre'],
            tags=line['Mots clés'],
            date_start=dateutil.parser.isoparse(line['Date de début']),
            longitude=lon,
            latitude=lat,
        ))
    db.session.commit()
    return render_template('index.html')


@app.route('/allEvent', methods=['GET'])
def describe_db():
    events = Event.query.all()
    for event in events:
        print(event.title_event)
    return render_template('index.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/nltkresponse', methods=['POST'])
def nltkresponse():
    #user_message = request.form['data']
    #print(user_message)
    results = {'message': "C'est noté !"}
    return jsonify(results)
