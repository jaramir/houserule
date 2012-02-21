#!/usr/bin/python
# coding: utf-8

from houserule import app
import os

if __name__ == "__main__":
    port = int( os.environ.get( "PORT", 5000 ) )
    app.run( "0.0.0.0", 5000 )

