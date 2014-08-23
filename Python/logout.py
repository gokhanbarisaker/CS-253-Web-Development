# -*- coding: UTF-8 -*-

import webapp2

class Handler(webapp2.RequestHandler):
  def get(self):
    self.response.headers.add_header('Set-Cookie', 'user=; Path=/')
    self.redirect('/unit4/signup')
