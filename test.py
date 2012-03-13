#!/usr/bin/python
# coding: utf-8

import os
os.environ["SECRET_KEY"] = "unittest"
os.environ["HEROKU_SHARED_POSTGRESQL_ORANGE_URL"] = "sqlite://"

import unittest
import houserule
import json

houserule.app.config["TESTING"] = True
houserule.app.config["CSRF_ENABLED"] = False

class TestWebApplication( unittest.TestCase ):
    # slow tests that interact with the application via simulated web requests

    def setUp( self ):
        houserule.db.create_all()
        self.client = houserule.app.test_client()

    def tearDown( self ):
        houserule.db.drop_all()

    def test_home_page_works( self ):
        r = self.client.get( '/' )
        self.assertTrue( r.data )
        self.assertEqual( r.status_code, 200 )

    def test_404_page( self ):
        r = self.client.get( '/i-am-not-found/' )
        self.assertEqual( r.status_code, 404 )

    def test_register( self ):
        data = {
            "username": "ciccio",
            "email": "ciccio@slack.it",
            "password": "cicciociccio",
            "verify": "cicciociccio",
        }
        r = self.client.post( "/register", data=data, follow_redirects=True )
        self.assertIn( "Grazie", r.data )

    def test_register_unique_username( self ):
        self.test_register()
        self.assertRaises( self.failureException, self.test_register )

    def test_login( self ):
        self.test_register()
        data = {
            "username": "ciccio",
            "password": "cicciociccio",
        }
        r = self.client.post( "/login", data=data, follow_redirects=True )
        self.assertIn( "Bentornato ciccio", r.data )

    def test_ciccio_is_the_one( self ):
        self.test_register()
        users = houserule.models.User.query.all()
        self.assertEqual( len( users ), 1 )
        self.assertEqual( users[0].id, 1 )
        self.assertEqual( users[0].username, "ciccio" )

    def test_match_requires_login( self ):
        r = self.client.post( "/match", data={} )
        self.assertEqual( 401, r.status_code )

    def test_create_match( self ):
        self.test_login()
        data = {
            "game_name": "Gioco dell'Oca",
            "location": "Club Esagonale",
            "user_id": "1",
        }
        r = self.client.post( "/match", data=data, follow_redirects=True )
        self.assertIn( "Grazie", r.data )
        # check that the data are here
        match = houserule.models.Match.query.first()
        self.assertEqual( match.game_name, data["game_name"] )
        self.assertEqual( match.location, data["location"] )
        self.assertEqual( match.user.username, "ciccio" )

if __name__ == '__main__':
    unittest.main()
