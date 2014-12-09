# -*- coding: UTF-8 -*-

from google.appengine.ext import db
from utilities import security

class User(db.Model):
  name = db.StringProperty(required = True)
  password = db.StringProperty(required = True)
  email = db.EmailProperty()

  def cookify(self):
    user_id = str(self.key().id())
    cookie_value = security.generate_hash(user_id)
    cookie = 'user={0}; Path=/'.format(cookie_value)
    return cookie
