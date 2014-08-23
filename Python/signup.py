# -*- coding: UTF-8 -*-

import webapp2
import re
import html
import security

username_regex = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
password_regex = re.compile(r"^.{3,20}$")
email_regex = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
  return username_regex.match(username)

def valid_password(password):
  return password_regex.match(password)

def valid_email(email):
  return email_regex.match(email)

class Unit2Handler(webapp2.RequestHandler):
  def get(self):
    self.response.out.write(html.render('signup.html'))
    #write_form(self.response.out)

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
      self.redirect("/unit2/welcome?username=" + username)

class Unit4Handler(webapp2.RequestHandler):
  def get(self):
    params = {
      "submit":"/unit4/signup"
    }
    self.response.out.write(html.render('signup.html', **params))
    #write_form(self.response.out)

  def post(self):
    username = self.request.get('username')
    password = self.request.get('password')
    verify = self.request.get('verify')
    email = self.request.get('email')

    params = {
      "username":username,
      "email":email,
      "submit":"/unit4/signup"
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
      cookie_value = security.generate_hash(username)
      cookie = 'username={0}; Path=/'.format(cookie_value)
      self.response.headers.add_header('Set-Cookie', cookie)
      self.redirect("/unit4/welcome")
