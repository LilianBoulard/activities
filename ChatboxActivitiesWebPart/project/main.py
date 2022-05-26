# main.py

from flask import Blueprint, render_template ,jsonify
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/nltkresponse', methods=['POST', 'GET'])
def nltkresponse():
    results = {'msg': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium chat box response'}
    return jsonify(results)