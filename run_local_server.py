#!/usr/bin/env python
# coding: utf-8

import argparse
import os

os.environ["HEROKU_SHARED_POSTGRESQL_ORANGE_URL"] = "sqlite:///../db.sqlite"
os.environ["SECRET_KEY"] = "development server not so secret key"

os.environ["GOOGLE_API_BROWSER_KEY"] = "AIzaSyAGPTwga_Nfc0PT6b8xICW9kDARu4o-5U8"

port = int( os.environ.get( "PORT", "5000" ) )

parser = argparse.ArgumentParser( description = "HouseRule Development Server" )
parser.add_argument( "--initdb", action="store_true", help="Create initial database" )
parser.add_argument( "--debug", action="store_true", help="Start with debugging and reloading" )
args = parser.parse_args()

from houserule import app, db

if args.initdb:
    print " * initializing db"
    db.create_all()

app.run( "0.0.0.0", port, debug=args.debug )
