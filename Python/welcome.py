# -*- coding: UTF-8 -*-

import webapp2
import html
import security
from user import User

class Unit2Handler(webapp2.RequestHandler):
  def get(self):
    user_name = self.request.get('username')
    self.response.out.write("Welcome, %s!" % html.escape(user_name))

class Unit4Handler(webapp2.RequestHandler):
  def get(self):
    user_hash = self.request.cookies.get('user')
    user_id = security.validate_hash(user_hash)

    if user_id:
      user = User.get_by_id(long(user_id))

      if user:
        self.response.out.write("Welcome, %s!" % html.escape(user.name))
      else:
          self.redirect("/unit4/signup")
    else:
      self.redirect("/unit4/signup")
