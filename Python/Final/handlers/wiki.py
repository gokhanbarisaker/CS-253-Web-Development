# -*- coding: UTF-8 -*-

import webapp2
from utilities import html
from utilities import authenticator
from models.wiki import Wiki

class Handler(webapp2.RequestHandler):
    def get(self, title):
        wiki = Wiki.get_by_title(title)

        if wiki:
            user = authenticator.authenticate(self.request)

            params = {
                "user":user,
                "wiki":wiki
            }

            output = html.render("wiki.html", **params)
            self.response.out.write(output)

        else:
            ## TODO: redirect to edit page
            self.redirect('/__edit' + title)
