# -*- coding: UTF-8 -*-

import webapp2
import html
import json
from google.appengine.api import memcache
from google.appengine.ext import db
import logging

CACHE_ARTS_KEY = 'arts'


class Art(db.Model):
  title = db.StringProperty(required = True)
  art = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)
  geopoint = db.GeoPtProperty()


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
      raw_arts = []

      for art in arts:

        raw_art = {
          "subject":art.title,
          "content":art.art,
          "created":art.created.strftime("%Y-%m-%d %H:%M:%S")
        }

        if art.geopoint:
          raw_art["geopoint"] = {
            "lat":art.geopoint.lat,
            "lon":art.geopoint.lon
          }

        raw_arts.append(raw_art)

      output = json.dumps(raw_arts)

    else:
      self.error(404)

    self.response.out.write(output)

  def post(self, unused):
    title = self.request.get('title')
    art = self.request.get('art')
    ll = self.request.headers.get('X-AppEngine-CityLatLong')
    geopoint = None

    if ll:
      geopoint_values = ll.split(',')
      geopoint = db.GeoPt(geopoint_values[0], geopoint_values[1])

    if title and art:
      #art = Art(title = title, art = art, geopoint = geopoint)
      self.add_art(title = title, art = art, geopoint = geopoint)

      self.redirect("/unit3/asciichan")
    else:
      arts = fetch_arts()

      params = {
        'title':title,
        'art':art,
        'arts':arts
      }

      self.response.out.write(html.render('asciichan.html', **params))


  def add_art(self, title, art, geopoint):

      art = Art(title = title, art = art, geopoint = geopoint)

      self.add_art_to_database(art)
      self.add_art_to_cache(art)


  def add_art_to_database(self, art):
      art.put()


  def add_art_to_cache(self, art):
      #CAS style cache update

      client = memcache.Client()
      while True: # Retry loop
          arts = client.gets(CACHE_ARTS_KEY)
          assert arts is not None, 'Uninitialized counter'
          arts.append(art)
          if client.cas(CACHE_ARTS_KEY, arts):
              break


  def fetch_arts(self, update = False):
    arts = None if update else memcache.get(CACHE_ARTS_KEY)

    # If cache does not contain arts
    if not arts:
      # Fetch arts from database
      arts = db.GqlQuery("select * from Art order by created desc")
      arts = list(arts)

      # Add to in-memory cache
      memcache.set(CACHE_ARTS_KEY, arts)

    return arts
