#!/usr/bin/env python3

import flask
from flask import Flask, jsonify
import pickle
import sys
import pandas

# Create the application.
APP = flask.Flask(__name__)

# read the data file
postal_codes = pickle.load(open(sys.argv[1], 'rb'))

@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('index.html')

#@APP.route('/hello/<name>/')
#def hello(name):
#    """ Displays the page greats who ever comes to visit it.
#    """
#    return flask.render_template('hello.html', name=name)

@APP.route('/api/v0.1/code/', methods=['GET'])
def random_code():
    random_code = postal_codes.sample().to_json(orient='records')
    response = APP.response_class(
        response=random_code,
        status=200,
        mimetype='application/json'
    )
    return response

@APP.route('/api/v0.1/code/<requestcode>/', methods=['GET'])
def get_code(requestcode):
    lookup_code = postal_codes.loc[postal_codes['POSTAL_CODE'] == requestcode].to_json(orient='records')

    #random_code = postal_codes.sample().to_json(orient='records')
    response = APP.response_class(
        response=lookup_code,
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    APP.debug=True
    APP.run()