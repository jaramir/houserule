#!/usr/bin/python
# coding: utf-8

import couchdbkit
import couchdbkit.loaders

class User( couchdbkit.Document ):
    username = couchdbkit.StringProperty()
    password = couchdbkit.StringProperty()
    email = couchdbkit.StringProperty()

def init( db ):
    # syncronize views
    path = "_design"
    loader = couchdbkit.loaders.FileSystemDocsLoader( path )
    loader.sync( db, verbose=True )

    # set db on documents
    User.set_db( db )
