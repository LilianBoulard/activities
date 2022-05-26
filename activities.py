import activities

from flask import Flask

app = Flask(__name__)


@app.route('/')
def application():
    return 'Hello World'


@app.route('/admin')
def admin_dashboard():
    return 'Not implemented !'


if __name__ == '__main__':
    app.run()
