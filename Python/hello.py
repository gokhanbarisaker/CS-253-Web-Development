# -*- coding: UTF-8 -*-

import webapp2
import html
import rot13
import signup
import welcome
import asciichan
import blog
import login
import logout

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
                    "day":    html.escape(day),
                    "month":  html.escape(month),
                    "year":   html.escape(year)})

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


application = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thanks', ThanksHandler),
    ('/unit2/rot13', rot13.Handler),
    ('/unit2/signup', signup.Unit2Handler),
    ('/unit4/signup', signup.Unit4Handler),
    ('/unit2/welcome', welcome.Unit2Handler),
    ('/unit4/welcome', welcome.Unit4Handler),
    (r'/unit3/asciichan(.*)', asciichan.Handler),
    (r'^/unit3/blog(\..*){0,1}$', blog.Handler),
    (r'/unit3/blog/(\d+)', blog.SingleEntryHandler),
    ('/unit3/blog/newpost', blog.NewPostHandler),
    ('/unit4/login', login.Handler),
    ('/unit4/logout', logout.Handler),
    ('/unit3/blog/signup', signup.Unit4Handler), ## For the sake of lame unit 6 problem set
    ('/unit3/blog/logout', signup.Unit4Handler), ## For the sake of lame unit 6 problem set
    ('/unit3/blog/flush', blog.FlushHandler)

], debug=True)
