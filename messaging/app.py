import json
import os
from flask import Flask, render_template
import flask
from message_helper import get_text_message_input, send_message

app = Flask(__name__)

# Get the directory of the current file to make config path relative to app location
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path) as f:
    config = json.load(f)

app.config.update(config)


@app.route("/")
def index():
    return render_template('index.html', name=__name__)


@app.route('/welcome', methods=['POST'])
async def welcome():
    data = get_text_message_input(app.config['RECIPIENT_WAID']
                                  , 'Welcome to the Flight Confirmation Demo App for Python!');
    await send_message(data)
    return flask.redirect(flask.url_for('index'))
