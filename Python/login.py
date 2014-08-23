# -*- coding: UTF-8 -*-

import webapp2
import html
import hashlib
from google.appengine.ext import db
from user import User

class Handler(webapp2.RequestHandler):
  def get(self):
    self.response.write(html.render('login.html'))

  def post(self):
    username = self.request.get('username')
    password = self.request.get('password')

    if username and password:
      user = db.GqlQuery("select * from User where name='{0}' limit 1".format(username)).get()

      if user and (user.password == hashlib.sha256(password).hexdigest()):
        cookie = user.cookify()
        self.response.headers.add_header('Set-Cookie', cookie)
        self.redirect('/unit4/welcome')

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
