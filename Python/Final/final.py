# -*- coding: UTF-8 -*-

import webapp2
from handlers import greet
from handlers import signup
from handlers import logout
from handlers import login
from handlers import wiki
from handlers import edit

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

application = webapp2.WSGIApplication([
    ('/', greet.Handler),
    ('/signup', signup.Handler),
    ('/logout', logout.Handler),
    ('/login', login.Handler),
    ('/__edit' + PAGE_RE, edit.Handler),
    (PAGE_RE, wiki.Handler)
], debug=True)
