#!/usr/bin/python
# coding: utf-8

from houserule import app, db
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from flaskext.login import login_user, logout_user, login_required, current_user
from utils import jsonify

import pyBGG
import forms
import models

@app.route( "/" )
def splash():
    return render_template( "splash.html" )

@app.route( "/index" )
def index():
    return render_template( "index.html" )

@app.route( "/register", methods=( "GET", "POST" ) )
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = models.User( form.username.data, form.password.data, form.email.data )
        db.session.add( user )
        db.session.commit()
        flash( "Grazie per esserti registrato!" )
        return redirect( url_for( "index" ) )
    return render_template( "register.html", form=form )

@app.route( "/login", methods=( "GET", "POST" ) )
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by( username=form.username.data ).first()
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
    form = forms.BGGTestForm()
    collection = []
    if form.validate_on_submit():
        collection = pyBGG.collection( form.username.data, own=True, prefetch=True )
    return render_template( "bggtest.html", form=form, collection=collection )

@app.route( "/match", methods=( "GET", "POST" ) )
@login_required
def match():
    form = forms.MatchForm()
    if form.validate_on_submit():

        # trova o crea il gioco
        game = models.Game.by_bgg_id( form.bgg_game_id.data )
        if not game:
            game = models.Game()
            game.bgg_id = form.bgg_game_id.data
            game.name = form.game_name.data
            db.session.add( game )

        # crea il match
        match = models.Match()
        match.game = game
        match.user = current_user
        db.session.add( match )

        # salva
        db.session.commit()

        flash( "Grazie per aver proposto una nuova partita!" )
        return redirect( url_for( "index" ) )

    return render_template( "match.html", form=form )

@app.route( "/search/game" )
@login_required
def ajax_game_search():
    term = request.args["term"]
    games = pyBGG.search( term, prefetch=True )
    rv = []
    for game in games:
        rv.append( {
            "name": game.name,
            "image": game.thumbnail,
        } )
    return jsonify( rv )
