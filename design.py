#!/usr/bin/python
# coding: utf-8

import couchdb
from couchdb.design import ViewDefinition

db_url = "http://localhost:5984/" # TODO leggi parametro dalla cmdline
db_name = "hr" # TODO leggi parametro dalla cmdline

couch = couchdb.Server( db_url ) 
db = couch[db_name] 

views = [
    ViewDefinition( "users", "by_username", """
        function( doc ) { 
            if( doc.username ) {
                emit( doc.username, doc );
            }
        } """ ),
    ]

ViewDefinition.sync_many( db, views, remove_missing=True )

