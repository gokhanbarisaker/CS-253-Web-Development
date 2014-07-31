# -*- coding: UTF-8 -*-

import webapp2
import html

def encode(s):
  alphabet_range = 26
  char_list = list(s)
  quantity = len(char_list)

  for i in range(0, quantity):
    char = char_list[i]
    char_int = ord(char)

    #uppercase
    if 65 <= char_int <= 90:
      char_int = ((char_int - 65 + 13) % alphabet_range) + 65
    #lowercase
    elif 97 <= char_int <= 122:
      char_int = ((char_int - 97 + 13) % alphabet_range) + 97

    char_list[i] = chr(char_int)

  return "".join(char_list)

class Handler(webapp2.RequestHandler):
  def get(self):
    params = {"text": ""}
    self.response.out.write(html.render('rot13.html', **params))

  def post(self):
    user_input = self.request.get('text')
    params = {"text": encode(user_input)}
    self.response.out.write(html.render('rot13.html', **params))
