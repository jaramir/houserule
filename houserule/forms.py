#!/usr/bin/python
# coding: utf-8

from flaskext.wtf import Form, validators, ValidationError
from flaskext.wtf import TextField, PasswordField, SubmitField, BooleanField
from flaskext.wtf.html5 import EmailField

from models import User
from houserule import bcrypt

class Unique( object ):
    """ Validator that checks field uniqueness
    http://librelist.com/browser//flask/2011/6/17/flask-wtforms-and-duplicate-ids/#f67efd2ff1bdab437b7a06c5d621a666
    """
    def __init__( self, model, field, message=None ):
        self.model = model
        self.field = field
        if not message:
            message = u'This element already exists'
        self.message = message

    def __call__( self, form, field ):
        check = self.model.query.filter( self.field == field.data ).first()
        if check:
            raise ValidationError( self.message )

class CheckPassword( object ):
    def __init__( self, message=None ):
        if not message:
            message = u'Nome utente o password errati'
        self.message = message

    def __call__( self, form, field ):
        user = User.query.filter_by( username=form.username.data ).first()

        if not user:
            raise ValidationError( self.message )

        if not bcrypt.check_password_hash( user.password, field.data ):
            raise ValidationError( self.message )


username_length = User.__table__.columns.username.type.length

class RegistrationForm( Form ):
    username = TextField( "Nome utente", [
        validators.Length( min=3, max=username_length, message="Il nome utente non deve eccedere i %d caratteri" % username_length ),
        Unique( User, User.username, message=u"Nome utente già in uso" ),
    ] )

    password = PasswordField( "Password", [
        validators.Length( min=8 ),
    ] )

    confirm = PasswordField( "Verifica la password", [
        validators.EqualTo( "confirm", message="Reinserisci la password" ),
    ] )

    email = TextField( "Indirizzo email", [
        validators.Email( "Indirizzo non valido" ),
    ] )

    submit = SubmitField( "Registrati" )

class LoginForm( Form ):
    username = TextField( "Nome utente", [
        validators.Length( min=3, max=username_length, message="Il nome utente non deve eccedere i %d caratteri" % username_length ),
    ] )

    password = PasswordField( "Password", [
        CheckPassword(),
    ] )

    remember = BooleanField( "Resta collegato" )

    submit = SubmitField( "Accedi" )

class BGGTestForm( Form ):
    username = TextField( "Nome utente BGG" )
    submit = SubmitField( "Elenca giochi" )

class MatchForm( Form ):
    submit = SubmitField( "Salva" )
