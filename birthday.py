import webapp2
import cgi
import re
import os



def escape_html(s):
	return cgi.escape(s, quote=True)

form = """
<form method="post">
		What is your birthday?
		<br>
		<input type="text" name="month" value="%(month)s">
		<input type="text" name="day" value="%(day)s">
		<input type="text" name="year" value="%(year)s">
		<div style="color: red">%(error)s</div>
		<br>
		<input type="submit">
	</form>
"""

months = ['January',
			  'February',
			  'March',
			  'April',
			  'May',
			  'June',
			  'July',
			  'August',
			  'September',
			  'October',
			  'November',
			  'December']

month_abbvs = dict((m[:3].lower(), m) for m in months)

def valid_month(month):
	if month:
		short_month = month[:3].lower()
		return month_abbvs.get(short_month)

def valid_day(day):
	if day and day.isdigit():
		day = int(day)
   		if day > 0 and day <= 31:
   			return day

def valid_year(year):
	if year and year.isdigit():
		year = int(year)
		if year >= 1900 and year <= 2020:
			return year

class BirthdayHandler(webapp2.RequestHandler):
	def write_form(self, error="", month="", day="", year=""):
		self.response.out.write(form % {"error": error,
										"month": escape_html(month),
										"day": escape_html(day),
										"year": escape_html(year)})

	def get(self):
		self.write_form()

	def post(self):
		user_month = self.request.get('month')
		user_day = self.request.get('day')
		user_year = self.request.get('year')

		month = valid_month(user_month)
		day = valid_day(user_day)
		year = valid_year(user_year)

		if not (month and day and year):
			self.write_form("YOU DUN' GOOFED!", 
							user_month, user_day, user_year)
		else:
			self.redirect("/birthday/thanks")

class ThanksHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Thanks nigga!")

app = webapp2.WSGIApplication([(r'/birthday/?', BirthdayHandler), (r'/birthday/thanks/?', ThanksHandler)],
                              debug=True)