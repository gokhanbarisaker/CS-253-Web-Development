# -*- coding: UTF-8 -*-

import webapp2
import html

class Handler(webapp2.RequestHandler):
  def get(self):
    user_name = self.request.get('username')
    self.response.out.write("Welcome, %s!" % html.escape(user_name))
