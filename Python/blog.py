# -*- coding: UTF-8 -*-

import webapp2
import html
from google.appengine.ext import db

class Entry(db.Model):
  subject = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
  def get(self):
    entries = db.GqlQuery('select * from Entry order by created desc limit 10')

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
      subject = self.request.get('subject')
      content = self.request.get('content')

      if subject and content:
        entry = Entry(subject=subject, content=content)
        entry.put()

        self.redirect("/unit3/blog/{0}".format(entry.key().id()))
      else:
        params = {
          'subject':subject,
          'content':content,
          'error':'We need both subject and content!'
        }

        self.response.write(html.render('newpost.html', **params))
