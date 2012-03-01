#!/usr/bin/python
# coding: utf-8

import argparse
import os

os.environ["HEROKU_SHARED_POSTGRESQL_ORANGE_URL"] = "sqlite:///../db.sqlite"
os.environ["SECRET_KEY"] = "development server not so secret key"

port = int( os.environ.get( "PORT", "5000" ) )

parser = argparse.ArgumentParser( description = "HouseRule Development Server" )
parser.add_argument( "--initdb", action="store_true", help="Create initial database" )
parser.add_argument( "--debug", action="store_true", help="Start with debugging and reloading" )
args = parser.parse_args()

from houserule import app, db

if args.initdb:
    db.create_all()

app.run( "0.0.0.0", port, debug=args.debug )
