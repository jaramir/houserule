#!/usr/bin/python
# coding: utf-8

class MockPyBGGBoardGame( object ):
    def __init__( self, *args, **kwargs ):
        self.__dict__ = kwargs

class MockPyBGG( object ):
    def search( self, term, prefetch=False ):
        return [
            MockPyBGGBoardGame( thumbnail="http://cf.geekdo-images.com/images/pic1115825_t.jpg", name="7 Wonders: Catan Island" ),
            MockPyBGGBoardGame( thumbnail="http://cf.geekdo-images.com/images/pic135066_t.jpg",  name="Catan Card Game" ),
            MockPyBGGBoardGame( thumbnail="http://cf.geekdo-images.com/images/pic976200_t.jpg",  name="Catan Dice Game" ),
            MockPyBGGBoardGame( thumbnail=None,                                                  name=u"Die Siedler von Catan - Th\u00fcringen Edition" ),
            MockPyBGGBoardGame( thumbnail="http://cf.geekdo-images.com/images/pic195977_t.jpg",  name="Simply Catan" ),
            MockPyBGGBoardGame( thumbnail="http://cf.geekdo-images.com/images/pic1210879_t.jpg", name="Star Trek Catan" ),
            MockPyBGGBoardGame( thumbnail="http://cf.geekdo-images.com/images/pic918589_t.jpg",  name="The Struggle for Catan" )
            ]

import sys
sys.modules["pyBGG"] = MockPyBGG()

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
            "bgg_game_id": "1001",
            "user_id": "1",
        }
        r = self.client.post( "/match", data=data, follow_redirects=True )
        self.assertIn( "Grazie", r.data )
        # check that the data are here
        match = houserule.models.Match.query.first()
        self.assertEqual( match.game.name, data["game_name"] )
        self.assertEqual( match.user.username, "ciccio" )

    def test_game_search( self ):
        # check the fixture in common with the client side
        with open( "static/fixture/search_game.json" ) as fp:
            fixture = json.load( fp )

        self.test_login()
        response = self.client.get( "/search/game?term=catan" )
        self.assertEqual( 200, response.status_code )
        data = json.loads( response.data )
        self.assertListEqual( data, fixture )


if __name__ == '__main__':
    unittest.main()
