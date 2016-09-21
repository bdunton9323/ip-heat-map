import tornado.ioloop
import tornado.web
import tornado.httpserver
import simplejson

import os
from socket import AF_INET

class GetDataHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)
    
    def set_default_headers(self):
    # TODO: change to 'http://localhost:8080' after I am done developing
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type, Origin, Accept")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        
    def get(self, *args, **kwargs):
        print "request: ", self.request.body
        lat1 = self.get_argument("lat1", None)
        long1 = self.get_argument("long1", None)
        lat2 = self.get_argument("lat2", None)
        long2 = self.get_argument("long2", None)
        print "point1: ", lat1, long1
        print "point2: ", lat2, long2
        
        points = [[35, -78, .2], 
            [35.97, -78.89, .2], 
            [35.97, -78.89, .2], 
            [35.97, -78.89, .2], 
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2]]
        response = {'data': points}
        self.write(response);
        
    def options(self, *args, **kwargs):
        print "handling options"
        #self.write('200')
        
def main():
    port = 8888

    application = tornado.web.Application([
        (r"/getdata", GetDataHandler),
        ],
        static_path = os.path.join(os.path.dirname(__file__), "static")
    )

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.bind(port, family=AF_INET)
    http_server.start(1)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()