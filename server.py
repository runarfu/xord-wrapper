#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Flask
from flask import jsonify

app = Flask(__name__)

import xord_wrapper

@app.route("/synonyms/<clue>", methods = ['GET'])
def get_synonyms(clue):
    return jsonify(xord_wrapper.lookup_all_synonyms(clue))

@app.route("/synonyms/<clue>/<int:length>", methods = ['GET'])
def get_synonyms_with_length(clue, length):
    return jsonify(xord_wrapper.lookup_synonyms_with_length(clue, length))

if __name__ == "__main__":
    app.debug = False
    app.run()

