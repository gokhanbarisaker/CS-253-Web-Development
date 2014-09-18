# -*- coding: UTF-8 -*-

import webapp2
import html
import json
from google.appengine.ext import db


class Art(db.Model):
  title = db.StringProperty(required = True)
  art = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)


class Handler(webapp2.RequestHandler):
  def get(self, suffix):
    output = ''
    arts = self.fetch_arts()

    if not suffix or suffix == '.html' or suffix == '.htm':
      params = {
        'arts':arts
      }

      output = html.render('asciichan.html', **params)

    elif suffix == '.json':
      raw_entries = []

      for art in arts:
        raw_entries.append({
          "subject":art.title,
          "content":art.art,
          "created":art.created.strftime("%Y-%m-%d %H:%M:%S")
        })

      output = json.dumps(raw_entries)

    else:
      self.error(404)

    self.response.out.write(output)

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
    arts = db.GqlQuery("select * from Art order by created desc")

    return list(arts)
