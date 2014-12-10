# -*- coding: UTF-8 -*-

import webapp2
from utilities import html
from utilities import authenticator
from models.wiki import Wiki
from google.appengine.ext import db

class Handler(webapp2.RequestHandler):
    def get(self, title):
        user = authenticator.authenticate(self.request)
        wiki = Wiki.get_by_title(title)

        if not wiki:
            # Create a fake wiki entry instance
            wiki = Wiki(**{
                'title':title,
                'body':''
            })

        params = {
            "user":user,
            "wiki":wiki
        }

        output = html.render("edit.html", **params)
        self.response.out.write(output)


    def post(self, title):

        ## Create new wiki

        Wiki(**{
            'title':title,
            'body':self.request.get('body')
        }).store()

        self.redirect(title)
