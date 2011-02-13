import tornado.web
import logging

class BaseHandler( tornado.web.RequestHandler ):
    pass

class FrontPageHandler( BaseHandler ):
    def get( self ):
        self.render( "index.html" )

