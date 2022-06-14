import dateutil
import pandas as pd

from flask import Flask

from activities.nlp import Model
from activities.utils import secret_key
from activities.database.sql import db
from activities.config import model_cookie_name
from activities.database.sql.models import Event

from flask import Blueprint, render_template, jsonify, request, session

app = Blueprint('app', __name__)


def create_app():
    root_app = Flask(__name__)

    # SQL database config
    root_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    root_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Session config
    #app.config['SESSION_FILE_DIR']
    #app.config['SESSION_FILE_THRESHOLD']
    #app.config['SESSION_FILE_MODE']
    root_app.config['SECRET_KEY'] = secret_key()

    db.init_app(root_app)

    root_app.register_blueprint(app)

    return root_app


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
            title_event=line['Titre'],  # TODO: rename to "title"
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
    # Create a new model instance
    model = Model()
    # Store the empty model in the session.
    # This also has the side effect of removing previously stored models.
    session[model_cookie_name] = model.to_json()
    return render_template('index.html')


@app.route('/nltkresponse', methods=['POST'])
def nltkresponse():
    user_message: str = request.get_json()
    # Get model information from the session.
    # If there is no stored information, creates a new model.
    model_info = session.get(model_cookie_name, '')
    # Create the model object from the info we got
    model = Model.from_json(model_info)
    if model.interpret_user_input(user_message):
        # The model has understood the message, and has updated the request.
        query_result = model.request.query()
        events = [event.to_json() for event in query_result]
    else:
        # In this case, the list of events on the web page should not change.
        # We pass None (json "null") to denote that.
        events = None

    results = {
        'message': f"J'ai bien noté {user_message!r}",
        'events': events
    }
    return jsonify(results)
