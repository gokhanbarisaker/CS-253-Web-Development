# -*- coding: UTF-8 -*-

import webapp2
import html
from google.appengine.ext import db


class Art(db.Model):
  title = db.StringProperty(required = True)
  art = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)


class Handler(webapp2.RequestHandler):
  def get(self):
    arts = self.fetch_arts()

    params = {
      'arts':arts
    }

    self.response.out.write(html.render('asciichan.html', **params))

  def post(self):
    title = self.request.get('title')
    art = self.request.get('art')

    if title and art:
      art = Art(title = title, art = art)
      art.put()

      self.redirect("/")
    else:
      arts = fetch_arts()

      params = {
        'title':title,
        'art':art,
        'arts':arts
      }

      self.response.out.write(html.render('asciichan.html', **params))

  def fetch_arts(self):
    return db.GqlQuery("select * from Art order by created desc")
