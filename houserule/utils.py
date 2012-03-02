#!/usr/bin/python
# coding: utf-8

import json
from flask import Response

def jsonify( data ):
    return Response( json.dumps( data ), mimetype="application/json" )