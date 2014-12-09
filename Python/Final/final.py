# -*- coding: UTF-8 -*-

import webapp2
from handlers import wiki


application = webapp2.WSGIApplication([
    ('/', wiki.GreetHandler),
    ('/signup', wiki.SignupHandler)
], debug=True)
