#!/usr/bin/python
# coding: utf-8

import os
import flask

app = flask.Flask( __name__ )

@app.route( '/' )
def hello():
    return flask.render_template( "index.html" )

if __name__ == '__main__':
    print "DB:", os.environ["HEROKU_SHARED_POSTGRESQL_ORANGE_URL"]

    port = int( os.environ.get( "PORT", 5000 ) )

    if os.environ.get( "DEBUG", "0" ) == "1":
        app.debug = True

    app.run( "0.0.0.0", port )
