#!/usr/bin/python
# coding: utf-8

import tornado.web
import logging
import uuid

def newid():
    return uuid.uuid4().hex

class BaseHandler( tornado.web.RequestHandler ):
    @property
    def db( self ):
        return self.application.db
        
    def get_current_user( self ):
        user_id = self.get_secure_cookie( "user" )
        if not user_id:
           return None
        return self.db.get( user_id )

class FrontPage( BaseHandler ):
    def get( self ):
        # TODO il message vuoto fa cagare
        self.render( "index.html", message="&nbsp;" )

class Profile( BaseHandler ):
    @tornado.web.authenticated
    def get( self ):
        self.render( "profile.html" )

class Login( BaseHandler ):
    def get( self ):
        self.render( "login.html", next=self.get_argument( "next", "/profile" ) )
        
    def post( self ):
        # TODO da fare via AJAX
        # TODO gestione errori
        username = self.get_argument( "username" )
        password = self.get_argument( "password" )
        rset = self.db.view( "users/by_username", key=username )
        if len( rset ) > 0 and rset.rows[0].value["password"] == password:
            self.set_secure_cookie( "user", rset.rows[0].id )
            self.redirect( self.get_argument( "next", "/profile" ) )
        else:
            self.render( "index.html", message="Nome utente o passoword errata" )
        
class Register( BaseHandler ):
    def post( self ):
        # TODO verifica che non esiste già un'utente con lo stesso nome
        # TODO non salvare la password in chiaro
        # TODO attivazione via email
        # TODO come gestire gli errori?
        self.db[newid()] = {
            "username": self.get_argument( "username" ),
            "password": self.get_argument( "password" ),
            "email": self.get_argument( "email" ),
            }
        self.render( "index.html", message="Il tuo account è stato creato. "
            "Riceverai a breve una e-mail con il link per l'attivazione." )

