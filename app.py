#!/usr/bin/python
# coding: utf-8

import os
import flask

app = flask.Flask( __name__ )

@app.route( '/' )
def hello():
    return flask.render_template( "index.html", debug=app.debug )

if __name__ == '__main__':
    port = int( os.environ.get( "PORT", 5000 ) )

    if "DEBUG" in os.environ:
        app.debug = True

    app.run( "0.0.0.0", port )
