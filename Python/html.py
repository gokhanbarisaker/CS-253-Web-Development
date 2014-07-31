# -*- coding: UTF-8 -*-

import os
import cgi
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def escape(s):
  return cgi.escape(s, quote=True)
  # s = s.replace("&", "&amp;")
  # s = s.replace("<", "&lt;")
  # s = s.replace(">", "&gt;")
  # s = s.replace('"', "&quot;")
  #
  # return s

def render(template, **params):
  t = jinja_env.get_template(template)
  return t.render(params)
