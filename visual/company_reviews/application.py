#!/usr/local/bin/python3.6

from flask import render_template
from flask import Flask

import pymongo
import sys
import os

sys.path.append('../../indeed_scrapper/indeed_scrapper.py')

app = Flask(__name__)
#app.config.from_object('config')

@app.route('/')
def main(name="Home"):
    return render_template('index.html', name=name)

@app.route('/index')
def index(name="Home"):
    return render_template('index.html', name=name)

@app.route('/topic_modeling')
def topic_modeling():
    return render_template('topic_modeling.html')

@app.route('/maps')
def maps():
    return render_template('maps.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
