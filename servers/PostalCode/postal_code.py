#!/usr/bin/env python3

import flask
from flask import Flask, jsonify
import pickle
import sys
import pandas as pd

# Create the application.
APP = flask.Flask(__name__)

# read the data file
postal_codes = pickle.load(open(sys.argv[1], 'rb'))

@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('index.html')

# Return a random postal code
@APP.route('/api/v0.1/code/', methods=['GET'])
def random_code():
    random_code = postal_codes.sample().to_json(orient='records')
    response = APP.response_class(
        response=random_code,
        status=200,
        mimetype='application/json'
    )
    return response

# return a specific postal code
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

# return a random Forward Sortation Area
@APP.route('/api/v0.1/fsa/', methods=['GET'])
def random_fsa():
    random_fsa =  (postal_codes.sample().FORWARD_SORTATION_AREA).to_frame().to_json(orient='records')
    response = APP.response_class(
        response=random_fsa,
        status=200,
        mimetype='application/json'
    )
    return response

# return postal codes in a Forward Sortation Area
@APP.route('/api/v0.1/fsa/<requestfsa>', methods=['GET'])
def get_fsa(requestfsa):
    code_list = list(postal_codes.loc[postal_codes['FORWARD_SORTATION_AREA'] == requestfsa ].POSTAL_CODE)
    code_json = pd.DataFrame({'POSTAL_CODES':[code_list]}).to_json(orient ='records')  
    #lookup_fsa = postal_codes.loc[postal_codes['FORWARD_SORTATION_AREA'] == requestfsa].to_json(orient='records')
    response = APP.response_class(
        response= code_json,
        status=200,
        mimetype='application/json'
    )
    return response
if __name__ == '__main__':
    APP.debug=True
    APP.run()