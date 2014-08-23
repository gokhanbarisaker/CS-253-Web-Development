# -*- coding: UTF-8 -*-

import webapp2
import html
import security

class Unit2Handler(webapp2.RequestHandler):
  def get(self):
    user_name = self.request.get('username')
    self.response.out.write("Welcome, %s!" % html.escape(user_name))

class Unit4Handler(webapp2.RequestHandler):
  def get(self):
    username_hash = self.request.cookies.get('username')
    user_name = security.validate_hash(username_hash)

    if user_name:
      self.response.out.write("Welcome, %s!" % html.escape(user_name))
    else:
      self.redirect("/unit4/signup")
