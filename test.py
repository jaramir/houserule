#!/usr/bin/python
# coding: utf-8

import unittest
import houserule

class TestApp( unittest.TestCase ):

    def setUp( self ):
        houserule.app.config["TESTING"] = True
        self.app = houserule.app.test_client()

    def test_home_page_works( self ):
        r = self.app.get( '/' )
        self.assertTrue( r.data )
        self.assertEquals( r.status_code, 200 )

    def test_404_page( self ):
        r = self.app.get( '/i-am-not-found/' )
        self.assertEquals( r.status_code, 404 )

    def test_user_loader( self ):
        self.assertEqual( self.app.load_user( "nonesiste" ), None )

if __name__ == '__main__':
    unittest.main()
