# -*- coding: UTF-8 -*-

import webapp2
import html
from google.appengine.ext import db

class Entry(db.Model):
  title = db.StringProperty(required = True)
  body = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
  def get(self):
    entries = db.GqlQuery('select * from Entry order by created desc')

    params = {
      'entries':entries
    }

    self.response.write(html.render('blog.html', **params))

class SingleEntryHandler(webapp2.RequestHandler):
  def get(self, identifier):
    entry = Entry.get_by_id(int(identifier))

    if entry:
      params = {
        'entries':[
          entry
        ]
      }

      self.response.write(html.render('blog.html', **params))

    else:
      self.response.write("<h1>No entry found!</h1>")

class NewPostHandler(webapp2.RequestHandler):
    def get(self):
      self.response.write(html.render('newpost.html'))
    def post(self):
      title = self.request.get('title')
      body = self.request.get('body')

      if title and body:
        entry = Entry(title=title, body=body)
        entry.put()

        self.redirect("/unit3/blog/{0}".format(entry.key().id()))
      else:
        params = {
          'title':title,
          'body':body,
          'error':'We need both title and body!'
        }

        self.response.write(html.render('newpost.html', **params))
