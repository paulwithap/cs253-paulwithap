import os
import webapp2
import jinja2
import urllib
import re
import cgi

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(template_dir))

class Tags(db.Model):
	name = db.StringProperty(required=True)
	time = db.DateTimeProperty(auto_now_add=True)

WORD_RE = re.compile(r'\b\w*\b')

def escape_html(s):
	return cgi.escape(s, quote=True)

def is_word(s):
	return WORD_RE.match(s)

def tagify(user_text):
	tag = ""
	tag_list = []
	for letter in user_text:
		if is_word(letter):
			tag+=letter
		else:
			tag_list.append(tag)
			tag = ""
	return tag_list


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
    	self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
    	t = jinja_env.get_template(template)
    	return t.render(params)

    def render(self, template, **kw):
    	self.write(self.render_str(template, **kw))

    def render_json(self, d):
    	json_txt = json.dumps(d)
    	self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
    	self.write(json_txt)

    def initialize(self, *a, **kw):
    	webapp2.RequestHandler.initialize(self, *a, **kw)

    	if self.request.url.endswith('.json'):
    		self.format = 'json'
    	else:
    		self.format = 'html'

class TagifyHandler(Handler):
	def render_page(self, user_text="", tags=""):
		self.render("tagify.html",
					user_text=user_text,
					tags=tags)

	def get(self):
		tags = db.GqlQuery("SELECT * FROM Tags ORDER BY time DESC LIMIT 1")
		self.render_page(tags=tags)

class PostHandler(Handler):

	def post(self):
		user_text = self.request.get('user_text')
		tag_list = tagify(user_text)
		name = ""
		for tag in tag_list:
			name+=tag+", "
		tags = Tags(name=name)
		tags.put()
		self.redirect('/tagify')
		

app = webapp2.WSGIApplication([(r'/tagify/?', TagifyHandler),
								(r'/tagify/post/?', PostHandler)],
                              debug=True)