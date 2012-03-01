#!/usr/bin/python
# coding: utf-8

import os
os.environ["SECRET_KEY"] = "unittest"

import unittest
import houserule

houserule.app.config["TESTING"] = True
houserule.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
houserule.app.config["CSRF_ENABLED"] = False

class TestApp( unittest.TestCase ):

    def setUp( self ):
        houserule.db.create_all()
        self.app = houserule.app.test_client()

    def tearDown( self ):
        houserule.db.drop_all()

    def test_home_page_works( self ):
        r = self.app.get( '/' )
        self.assertTrue( r.data )
        self.assertEquals( r.status_code, 200 )

    def test_404_page( self ):
        r = self.app.get( '/i-am-not-found/' )
        self.assertEquals( r.status_code, 404 )

    def test_register( self ):
        data = {
            "username": "ciccio",
            "email": "ciccio@slack.it",
            "password": "cicciociccio",
            "verify": "cicciociccio",
        }
        r = self.app.post( "/register", data=data, follow_redirects=True )
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
        r = self.app.post( "/login", data=data, follow_redirects=True )
        self.assertIn( "Bentornato ciccio", r.data )

    def test_ciccio_is_the_one( self ):
        self.test_register()
        users = houserule.models.User.query.all()
        self.assertEqual( len( users ), 1 )
        self.assertEqual( users[0].id, 1 )
        self.assertEqual( users[0].username, "ciccio" )

    def test_match_requires_login( self ):
        r = self.app.post( "/match", data={} )
        self.assertEqual( "401 UNAUTHORIZED", r.status )

    def test_create_match( self ):
        self.test_login()
        data = {
            "bgg_id": "421",
            "name": "1830: Railways & Robber Barons",
            "thumbnail": "http://cf.geekdo-images.com/images/pic882119_t.jpg",
            "user_id": "1",
        }
        r = self.app.post( "/match", data=data, follow_redirects=True )
        self.assertIn( "Grazie", r.data )

if __name__ == '__main__':
    unittest.main()
