# -*- coding: UTF-8 -*-

import webapp2
from utilities import html

class GreetHandler(webapp2.RequestHandler):
    def get(self):
        params = {}

        output = html.render('greet.html', **params)
        self.response.out.write(output)
