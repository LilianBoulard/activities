from flask import Blueprint, render_template, jsonify

app = Blueprint('main', __name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/nltkresponse', methods=['POST', 'GET'])
def nltkresponse():
    results = {'msg': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium chat box response'}
    return jsonify(results)
