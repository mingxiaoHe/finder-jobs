#!/usr/bin/env python
# coding=utf-8

import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen

from tornado.options import define, options
from modules.LagouAPI import GetJob
from modules.SqlHelper import SqlHelper

define('port', default=80, help='run on the given port', type=int)

class BaseHandler(tornado.web.RequestHandler):
    pass

class IndexHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('index.html')

class AboutHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('about.html')

class ApiJobsHandler(BaseHandler):
    def get(self):
        self.write(json.dumps(GetJob(), ensure_ascii=False))

if __name__ == '__main__':
    # SqlHelper()
    tornado.options.parse_command_line()
    settings = {
        'template_path':  os.path.join(os.path.dirname(__file__), 'templates'),
        'static_path':  os.path.join(os.path.dirname(__file__), 'static'),
        'libs': os.path.join(os.path.dirname(__file__), 'libs'),
    }
    app = tornado.web.Application(
        handlers = [
            (r'/', IndexHandler),
            (r'/about', AboutHandler),
            (r'/api/jobs', ApiJobsHandler),
        ], **settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
