# -*- coding: UTF-8 -*-

import webapp2
import cgi
import rot13

form = """
<form method="post" action="/">
  <label>
    Day
    <input type="text" name="day" value="%(day)s">
  </label>
  <label>
    Month
    <input type="text" name="month" value="%(month)s">
  </label>
  <label>
    Year
    <input type="text" name="year" value="%(year)s">
  </label>
  <div style="color: red">%(error)s</div>
  <br>
  <br>
  <input type="submit">
</form>
"""

rot13_form = """
<form method="post" action="/unit2/rot13">
  <label>
    Rot13
    <textarea name="text" rows="10" cols="50">%(text)s</textarea>
  </label>
  <br>
  <br>
  <input type="submit">
</form>
"""

months = {
  'jan':'January',
  'feb':'February',
  'mar':'March',
  'apr':'April',
  'may':'May',
  'jun':'June',
  'jul':'July',
  'aug':'August',
  'sep':'September',
  'oct':'October',
  'nov':'November',
  'dec':'December',
}

def valid_day(day):
    if day and day.isdigit():
      dayInt = int(day)
      if (dayInt < 31) and (dayInt > 0):
        return dayInt

def valid_month(month):
  if month:
    monthSimplified = month[:3].lower()
    return months.get(monthSimplified, None)

def valid_year(year):
  if year and year.isdigit():
    yearInt = int(year)
    if (yearInt > 1800) and (yearInt <2200):
      return yearInt

def write_form(out, error="", day="", month="", year=""):
  out.write(form % {"error":  error,
                    "day":    escape_html(day),
                    "month":  escape_html(month),
                    "year":   escape_html(year)})

def escape_html(s):
  return cgi.escape(s, quote=True)
  # s = s.replace("&", "&amp;")
  # s = s.replace("<", "&lt;")
  # s = s.replace(">", "&gt;")
  # s = s.replace('"', "&quot;")
  #
  # return s

class MainHandler(webapp2.RequestHandler):
  def get(self):
    #self.response.headers['Content-Type'] = 'text/plain'
    write_form(self.response.out)

  def post(self):
    user_day = self.request.get('day')
    user_month = self.request.get('month')
    user_year = self.request.get('year')

    day = valid_day(user_day)
    month = valid_month(user_month)
    year = valid_year(user_year)

    if day and month and year:
      self.redirect("/thanks")
    else:
      write_form(self.response.out, 'This, my friend, is wrong. Just, wrong!', user_day, user_month, user_year)


class ThanksHandler(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('Brilliant!')

class Rot13Handler(webapp2.RequestHandler):
  def get(self):
    self.response.out.write(rot13_form % {"text": escape_html("")})

  def post(self):
    user_input = self.request.get('text')
    self.response.out.write(rot13_form % {"text": escape_html(rot13.encode(user_input))})

application = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thanks', ThanksHandler),
    ('/unit2/rot13', Rot13Handler)
], debug=True)
