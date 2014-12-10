# -*- coding: UTF-8 -*-

import webapp2
import hashlib
from utilities import html
from models.user import User

from google.appengine.ext import db

class Handler(webapp2.RequestHandler):
    def get(self):
        self.response.write(html.render('login.html'))

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        if username and password:
            #User.all().filter('name =', username).get()
            user = db.GqlQuery("select * from User where name='{0}' limit 1".format(username)).get()

            if user and (user.password == hashlib.sha256(password).hexdigest()):
                cookie = user.cookify()
                self.response.headers.add_header('Set-Cookie', cookie)
                self.redirect('/')

            else:
                params = {
                'error':'invalid login',
                'username':username
                }
                self.response.write(html.render('login.html', **params))

        else:
            params = {
                'error':'invalid login',
                'username':username
            }
            self.response.write(html.render('login.html', **params))
