from activities.nlp import Model, NLP
from activities.database.redis import Event
from activities.config import behind_reverse_proxy
from activities.utils import secret_key, decode_json

from typing import List
from random import shuffle
from flask import Flask, Blueprint, render_template, jsonify, request, session


app = Blueprint('app', __name__,
                static_folder='static', template_folder='templates',
                url_prefix='/activities' if behind_reverse_proxy else '')


def create_app():
    root_app = Flask(__name__)

    # SQL database config
    root_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    root_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # For reverse proxy
    if behind_reverse_proxy:
        root_app.config['APPLICATION_ROOT'] = '/activities'

    # Session config
    #app.config['SESSION_FILE_DIR']
    #app.config['SESSION_FILE_THRESHOLD']
    #app.config['SESSION_FILE_MODE']
    root_app.config['SECRET_KEY'] = secret_key()

    root_app.register_blueprint(app)

    return root_app


# Create the NLP model so that it is loaded when the server starts, and not
# when the first message is received
_nlp = NLP()


def get_events(model: Model) -> List[Event]:
    return [event.to_json() for event in model.request.query()]


@app.route('/get_all_events', methods=['POST'])
def get_all_events():
    # Use an empty model to query, returning all events
    model = Model()
    events = get_events(model)[:100]
    shuffle(events)
    return jsonify({'events': events})


@app.route('/')
def index():
    # Create a new model instance
    model = Model()
    # Store the empty model in the session.
    # This also has the side effect of removing previously stored models.
    session['model_info'] = model.to_json()
    return render_template('index.html')


@app.route('/nlp', methods=['POST'])
def nlp():
    user_message: str = request.get_json()
    # Get model information from the session.
    # If there is no stored information, creates a new model.
    model_info = session.get('model_info', '')
    # Create the model object from the info we got
    model = Model.from_json(decode_json(model_info))
    understood_something, answer = model.interpret_user_input(user_message)
    if understood_something:
        # Save the updated model in the session
        session['model_info'] = model.to_json()
        # The model has understood the message, and has updated the request.
        matching_events = get_events(model)
    else:
        # In this case, the list of events on the web page should not change.
        # We pass None (json "null") to denote that.
        matching_events = []

    return jsonify({
        'message': answer,
        'events': matching_events,
    })


@app.route('/get_request_info', methods=['POST'])
def get_request_info():
    model_info = session.get('model_info', '')
    model = Model.from_json(decode_json(model_info))
    return jsonify(model.request.get_fields_desc())
