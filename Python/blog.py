# -*- coding: UTF-8 -*-

import webapp2
import html
import json
from google.appengine.ext import db
import logging

class Entry(db.Model):
  subject = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
  def get(self, suffix):

    output = ''
    entries = self.recent_entries()

    if not suffix or suffix == '.html' or suffix == 'htm':
      params = {
        'entries':entries
      }

      output = html.render('blog.html', **params)

    elif suffix == '.json':
      raw_entries = []

      for entry in entries:
        raw_entries.append({
          "subject":entry.subject,
          "content":entry.content,
          "created":entry.created.strftime("%Y-%m-%d %H:%M:%S")
        })

      output = json.dumps(raw_entries)

    else:
      self.error(404)

    self.response.out.write(output)

  def recent_entries(self):
    entries = db.GqlQuery('select * from Entry order by created desc limit 10')

    return list(entries)


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
