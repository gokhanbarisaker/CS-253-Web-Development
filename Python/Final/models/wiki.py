# -*- coding: UTF-8 -*-

from google.appengine.ext import db
from google.appengine.api import memcache

class Wiki(db.Model):
    title = db.StringProperty(required = True)
    body = db.StringProperty()

    def store(self):
        self.put()
        memcache.set(self.title, self)

    @staticmethod
    def get_by_title(title):

        wiki = memcache.get(title)

        if not wiki:
            wiki = db.GqlQuery("select * from Wiki where title='{0}' limit 1".format(title)).get()

        return wiki
