# -*- coding: UTF-8 -*-

import security

from google.appengine.ext import db

class User(db.Model):
  name = db.StringProperty(required = True)
  password = db.StringProperty(required = True)
  email = db.EmailProperty()

  def cookify(self):
    user_id = str(self.key().id())
    cookie_value = security.generate_hash(user_id)
    cookie = 'user={0}; Path=/'.format(cookie_value)
    return cookie
