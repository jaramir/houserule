#!/usr/bin/python
# coding: utf-8

from houserule import db
from houserule import bcrypt

from flaskext.login import UserMixin

class User( db.Model, UserMixin ):
    __tablename__ = "users"

    id = db.Column( db.Integer, primary_key=True )
    username = db.Column( db.String( 60 ), index=True, unique=True )
    password = db.Column( db.String( 60 ) )
    email = db.Column( db.String( 200 ) )

    def __init__( self, username, password, email ):
        self.username = username
        self.password = bcrypt.generate_password_hash( password )
        self.email = email

class Match( db.Model ):
    __tablename__ = "matches"

    id = db.Column( db.Integer, primary_key=True )

    user_id = db.Column( db.Integer, db.ForeignKey( "users.id" ) )
    user = db.relationship( "User" )

    game_name = db.Column( db.String( 150 ) )
    location = db.Column( db.String( 250 ) )
