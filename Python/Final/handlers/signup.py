# -*- coding: UTF-8 -*-

import webapp2
import re
import hashlib
from utilities import html
from models.user import User

username_regex = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
password_regex = re.compile(r"^.{3,20}$")
email_regex = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
  return username_regex.match(username)

def valid_password(password):
  return password_regex.match(password)

def valid_email(email):
  return email_regex.match(email)

class Handler(webapp2.RequestHandler):
    def get(self):
        # TODO: Add signup redirect query parameter. e.g .../signup?r=originUrl
        # which will later be carried over form parameters and will be redirected after success

        output = html.render('signup.html')
        self.response.out.write(output)

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = {
          "username":username,
          "email":email
        }

        error_detected = False

        if not valid_username(username):
          params['username_error'] = "Username is invalid"
          error_detected = True

        if not (password == verify):
          params['verify_error'] = "Password does not match"
          error_detected = True
        elif not valid_password(verify):
          params['password_error'] = "Password is invalid"
          error_detected = True

        if email and not valid_email(email):
          params['email_error'] = "Email is invalid"
          error_detected = True

        if error_detected:
          self.response.out.write(html.render('signup.html', **params))
        else:
          #TODO use salt by hashing (pass + salt) and storing as hash|salt

          params = {
            'name':username,
            'password':hashlib.sha256(password).hexdigest()
          }

          if email:
            params['email'] = db.Email(email)

          user = User(**params)
          user.put()
          cookie = user.cookify()
          self.response.headers.add_header('Set-Cookie', cookie)
          self.redirect("/")
