#!/usr/bin/python
# coding: utf-8

from houserule import app, db
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from form import RegistrationForm, LoginForm, BGGTestForm
from model import User
from flaskext.login import login_user, logout_user, login_required, current_user
import pyBGG

@app.route( "/" )
def splash():
    return render_template( "splash.html" )

@app.route( "/index" )
def index():
    return render_template( "index.html" )

@app.route( "/register", methods=( "GET", "POST" ) )
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User( form.username.data, form.password.data, form.email.data )
        db.session.add( user )
        db.session.commit()
        flash( "Grazie per esserti registrato!" )
        return redirect( url_for( "index" ) )
    return render_template( "register.html", form=form )

@app.route( "/login", methods=( "GET", "POST" ) )
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by( username=form.username.data ).first()
        login_user( user, remember=form.remember.data )
        flash( "Bentornato %s!" % user.username )
        return redirect( request.args.get( "next" ) or url_for( "index" ) )
    return render_template( "login.html", form=form )

@app.route( "/logout" )
@login_required
def logout():
    logout_user()
    flash( "Buon gioco!" )
    return redirect( url_for( "index" ) )

@app.route( "/bggtest", methods=( "GET", "POST" ) )
@login_required
def bggtest():
    form = BGGTestForm()
    collection = []
    if form.validate_on_submit():
        collection = pyBGG.collection( form.username.data, own=True, prefetch=True )
    return render_template( "bggtest.html", form=form, collection=collection )

#@app.route( "/initdb" )
#@login_required
#def initdb():
#    db.create_all()
#    return redirect( url_for( "index" ) )
