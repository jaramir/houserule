#!/usr/bin/python

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line
from tornado.web import Application
from houserule.handlers import FrontPageHandler

# local options
define( "db_url", default="http://localhost/hr", help="CouchDB URL", type=str )
define( "port", default=8888, help="Listening port", type=int )

class Houserule( Application ):
    def __init__( self ):
        handlers = (
            ( r"/", FrontPageHandler ),
            )
        settings = {
            "xsrf_cookies": True,
            "debug": True,
            "static_path": "static",
            "template_path": "templates",
            }
        Application.__init__( self, handlers, **settings )

if __name__ == "__main__":
    parse_command_line() # enables logging to stdout!
    options["logging"].set( "debug" )
    http_server = HTTPServer( Houserule() )
    http_server.listen( options.port )
    print "Listening on port %s" % options.port
    IOLoop.instance().start()

