import pandas as pd
from .database.sql import db
from .database.sql.models import Event

import dateutil
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from flask import Blueprint, render_template, jsonify

app = Blueprint('app', __name__)

#Session = sessionmaker(bind=db)

@app.route('/newEvent',methods=['GET'])
def populate_db():
    new_event= Event(id=1,title_event="cinema",tags="tag_cinema",date_start=datetime(1988,1,17),latitude=3,longitude=5)
    db.session.add(new_event)
    db.session.commit()
    return render_template('index.html')

@app.route('/allEvent',methods=['GET'])
def describe_db():
    events=Event.query.all()
    for event in events:
        print(event.title_event)
    return render_template('index.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/nltkresponse', methods=['POST', 'GET'])
def nltkresponse():
    results = {'msg': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium chat box response'}
    return jsonify(results)

