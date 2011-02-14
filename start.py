#!/usr/bin/python
# coding: utf-8

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line
from tornado.web import Application
import houserule.handlers
import couchdb

def generate_cookie_secret():
    # https://gist.github.com/823887
    import base64
    import uuid
    return base64.b64encode( uuid.uuid4().bytes + uuid.uuid4().bytes )

# local options
define( "db_url", default="http://localhost:5984/", help="CouchDB URL", type=str )
define( "db_name", default="hr", help="CouchDB Database Name", type=str )
define( "port", default=8888, help="Listening port", type=int )

class Houserule( Application ):
    def __init__( self ):
        handlers = (
            ( "/", houserule.handlers.FrontPage ),
            ( "/login", houserule.handlers.Login ),
            ( "/register", houserule.handlers.Register ),
            ( "/profile", houserule.handlers.Profile ),
            )
        settings = {
            "xsrf_cookies": True,
            "debug": True,
            "static_path": "static",
            "template_path": "templates",
            "cookie_secret": generate_cookie_secret(),
            "login_url": "/login",
            }
        Application.__init__( self, handlers, **settings )
        
        couch = couchdb.Server( options.db_url )
        if not options.db_name in couch:
            couch.create( options.db_name )
        self.db = couch[options.db_name]

if __name__ == "__main__":
    parse_command_line() # enables logging to stdout!
    options["logging"].set( "debug" )
    http_server = HTTPServer( Houserule() )
    http_server.listen( options.port )
    print "Listening on port %s" % options.port
    IOLoop.instance().start()

