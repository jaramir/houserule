#!/usr/bin/python
# coding: utf-8

import os
import flask
import urlparse

app = flask.Flask( __name__ )

global db
db=False

@app.route( '/' )
def hello():
    return flask.render_template( "index.html", db=db )

if __name__ == '__main__':

    db = urlparse.urlparse( os.environ["DATABASE_URL"] )

    port = int( os.environ.get( "PORT", 5000 ) )

    if os.environ.get( "DEBUG", "0" ) == "1":
        app.debug = True

    app.run( "0.0.0.0", port )
