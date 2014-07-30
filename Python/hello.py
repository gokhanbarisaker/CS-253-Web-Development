# -*- coding: UTF-8 -*-

import webapp2

form = """
<form method="post" action="/">
  <label>
    Day
    <input type="text" name="day">
  </label>
  <label>
    Month
    <input type="text" name="month">
  </label>
  <label>
    Year
    <input type="text" name="year">
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
    return months[monthSimplified]

def valid_year(year):
  if year and year.isdigit():
    yearInt = int(year)
    if (yearInt > 1800) and (yearInt <2200):
      return yearInt

def write_form(out, error=""):
  out.write(form % {"error": error})

class MainPage(webapp2.RequestHandler):
  def get(self):
    #self.response.headers['Content-Type'] = 'text/plain'
    write_form(self.response.out)

  def post(self):
    day = valid_day(self.request.get('day'))
    month = valid_month(self.request.get('month'))
    year = valid_year(self.request.get('year'))

    if day and month and year:
      self.response.out.write('Brilliant!')
    else:
      write_form(self.response.out, 'This, my friend, is wrong. Just, wrong!')

application = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
