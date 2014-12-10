# -*- coding: UTF-8 -*-

import webapp2
from utilities import html
from utilities import authenticator

class Handler(webapp2.RequestHandler):
    def get(self):
        user = authenticator.authenticate(self.request)

        params = {
            "user":user
        }

        output = html.render('greet.html', **params)
        self.response.out.write(output)
