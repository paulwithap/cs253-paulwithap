import os
import webapp2
import jinja2
import urllib
import re
import cgi

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(template_dir))

def rot13(text):
    output = ''
    for letter in text:
        if letter.isalpha():
            if letter.islower():
                if ord(letter) <= ord('m'):
                    output += chr(ord(letter)+13)
                else:
                    output += chr(ord(letter)-13)
            else:
                if ord(letter) <= ord('M'):
                    output += chr(ord(letter)+13)
                else:
                    output += chr(ord(letter)-13)
        else:
            output += letter
    return output

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

class Rot13Handler(Handler):
    def get(self, text=""):
        self.render('rot13.html', text=text)

    def post(self, text="", ouput=""):
        text = self.request.get('text')
        text = rot13(text)
        self.render('rot13.html', text=text)

app = webapp2.WSGIApplication([(r'/rot13/?', Rot13Handler)],
                              debug=True)