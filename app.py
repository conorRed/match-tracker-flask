import os
from flask import Flask, json
from flask import render_template
import pandas as pd
from flask import jsonify
from jinja2 import Environment
from flask_cors import CORS

app = Flask(__name__)
app.jinja_options['extensions'].append('jinja2.ext.loopcontrols')

CORS(app)


@app.route('/api/teams')
def return_team_sheets():
    ts1 = json.load(open("config/team_sheet1.json"))
    ts2 = json.load(open("config/team_sheet2.json"))
    team_sheets = [ts1, ts2]
    return jsonify(team_sheets)


@app.route('/api/events')
def return_events():
    events = json.load(open("config/events.json"))
    return jsonify(events)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
