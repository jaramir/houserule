#!/usr/bin/python
# coding: utf-8

from houserule import app, db
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description = "HouseRule Development Server" )
    parser.add_argument( "--initdb", action="store_true", help="Create initial database" )
    args = parser.parse_args()

    if args.initdb:
        db.create_all()

    port = int( os.environ.get( "PORT", "5000" ) )
    app.run( "0.0.0.0", port )

