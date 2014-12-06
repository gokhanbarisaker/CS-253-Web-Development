# -*- coding: UTF-8 -*-

import webapp2
import html
import json
from google.appengine.api import memcache
from google.appengine.ext import db
import logging
import time

CACHE_ENTRIES_KEY = 'entries'
CACHE_TIMESTAMP_KEY = 'timestampo'

class Entry(db.Model):
  subject = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
  def get(self, suffix):

    output = ''
    entries = recent_entries(False)

    if not suffix or suffix == '.html' or suffix == 'htm':
      params = {
        'queryTimeElapsed':elapsed_time(),
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


class SingleEntryHandler(webapp2.RequestHandler):
  def get(self, identifier):
    entry = Entry.get_by_id(int(identifier))

    if entry:
      params = {
        'queryTimeElapsed':elapsed_time(identifier),
        'entries':recent_entries(identifier = identifier)
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
        add_entry(entry)

        self.redirect("/unit3/blog/{0}".format(entry.key().id()))
      else:
        params = {
          'subject':subject,
          'content':content,
          'error':'We need both subject and content!'
        }

        self.response.write(html.render('newpost.html', **params))


class FlushHandler(webapp2.RequestHandler):
  def get(self):
    memcache.flush_all()
    self.redirect("/unit3/blog")


def add_entry(entry, namespace = None):
    add_entry_to_database(entry)
    add_entry_to_cache(entry, namespace)


def add_entry_to_database(entry):
    add_entries_to_database([entry])


def add_entries_to_database(entries):
    for entry in entries:
        entry.put()


def add_entry_to_cache(entry, namespace = None):
    add_entries_to_cache([entry], namespace)


def add_entries_to_cache(entries, namespace = None):
    #CAS style cache update

    client = memcache.Client()
    for x in range(0, 5): # Retry loop
        # cached_entries = client.gets(CACHE_ENTRIES_KEY)
        cache = client.get_multi([CACHE_ENTRIES_KEY, CACHE_TIMESTAMP_KEY], namespace = namespace, for_cas = True)
        cached_entries = cache.get(CACHE_ENTRIES_KEY)

        timestamp = int(round(time.time()))

        if cached_entries is None:
            logging.info('Creating new entry list!')

            updateMap = {
                CACHE_ENTRIES_KEY:entries,
                CACHE_TIMESTAMP_KEY:timestamp
            }

            # !!!: Note to future self,
            # If memcache key not inserted before, cas related methods tend to fail
            #
            client.set_multi(updateMap, namespace = namespace)
            break

        else:
            cached_entries.extend(entries)

            updateMap = {
                CACHE_ENTRIES_KEY:cached_entries,
                CACHE_TIMESTAMP_KEY:timestamp
            }


            failedKeys = client.cas_multi(updateMap, namespace = namespace)

            if not failedKeys:
                logging.info('Updated cache @{0}'.format(timestamp))
                break
            else:
                logging.info('Cache update failed for keys: {0}'.format(failedKeys))

        logging.info('CAS retry!')

    logging.error('Memcache is on strike!')


def elapsed_time(identifier = None):
  timestamp = 0

  if identifier:
      timestamp = memcache.get(CACHE_TIMESTAMP_KEY, namespace = identifier)
  else:
      timestamp = memcache.get(CACHE_TIMESTAMP_KEY)

  if timestamp is None:
      logging.info('Cache does not posses timestamp!')
      return 0

  return int(round(time.time())) - timestamp


def recent_entries(update = False, identifier = None):
  entries = None if update else memcache.get(CACHE_ENTRIES_KEY, namespace = identifier)

  # If cache does not contain entries
  if not entries:
    logging.info('Cache miss!')

    whereCondition = "where __key__ = KEY('Entry', {0})".format(identifier) if identifier else ''

    # Fetch entries from database
    entries = db.GqlQuery('select * from Entry {0} order by created desc limit 10'.format(whereCondition))
    entries = list(entries)

    # Add to in-memory cache
    add_entries_to_cache(entries, identifier)

  return entries
