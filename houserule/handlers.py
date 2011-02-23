#!/usr/bin/python
# coding: utf-8

import tornado.web
import logging
import couchdbkit
from model import User

class BaseHandler( tornado.web.RequestHandler ):
    @property
    def db( self ):
        return self.application.db
        
    def get_current_user( self ):
        user_id = self.get_secure_cookie( "user" )
        if not user_id:
           return None
        return User.get( user_id )

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
        user = User.view( "users/by_username", key=username ).one()
        if user and user.verify_password( password ):
            self.set_secure_cookie( "user", user._id )
            self.redirect( self.get_argument( "next", "/profile" ) )
        else:
            self.render( "index.html", message="Nome utente o passoword errata" )

class Logout( BaseHandler ):
    def get( self ):
        self.clear_cookie( "user" )
        self.redirect( self.get_argument( "next", "/" ) )

class Register( BaseHandler ):
    def post( self ):
        # TODO attivazione via email
        # TODO come gestire gli errori?

        username = self.get_argument( "username" )
        password = self.get_argument( "password" )
        email = self.get_argument( "email" )
        
        # verifica che non esiste già un'utente con lo stesso nome
        user = User.view( "users/by_username", key=username ).one()
        if user:
            self.render( "index.html", message="Esiste già un'account con questo nome" )
            return
        
        user = User()
        user.username = username
        user.password = User.hash_password( password )
        user.email = email
        user.save()

        self.render( "index.html", message="Il tuo account è stato creato. "
            "Riceverai a breve una e-mail con il link per l'attivazione." )
