#!/usr/bin/python
# coding: utf-8

import couchdb
from couchdb.design import ViewDefinition

def sync_db( db ):
    views = [
        ViewDefinition( "users", "by_username", """
            function( doc ) { 
                if( doc.username ) {
                    emit( doc.username, doc );
                }
            } """ ),
        ]
    ViewDefinition.sync_many( db, views, remove_missing=True )

if __name__ == "__main__":
    sync_db( couchdb.Server()["hr"] )
