#!/usr/bin/python
# coding: utf-8

import couchdbkit
import couchdbkit.designer
import bcrypt
BCRYPT_COST=12

class User( couchdbkit.Document ):
    username = couchdbkit.StringProperty()
    password = couchdbkit.StringProperty()
    email = couchdbkit.StringProperty()

    @staticmethod
    def hash_password( password ):
        # generate random salt with given cost
        return bcrypt.hashpw( password, bcrypt.gensalt( BCRYPT_COST ) )
    
    def verify_password( self, password ):
        # uses saved salt
        return bcrypt.hashpw( password, self.password ) == self.password
    
def init( db ):
    # syncronize views
    couchdbkit.designer.push( "_design", db )

    # set db on documents
    User.set_db( db )
