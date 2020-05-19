# coding: utf-8


from urlparse import urlparse
from datetime import datetime
import flask
import requests_toolbelt.adapters.appengine

import config
import util

# Enable requests compatibility with GAE (needed for authlib)
# From https://toolbelt.readthedocs.io/en/latest/adapters.html#appengineadapter
requests_toolbelt.adapters.appengine.monkeypatch()


class GaeRequest(flask.Request):
  trusted_hosts = config.TRUSTED_HOSTS


app = flask.Flask(__name__)
app.config.from_object(config)
app.request_class = GaeRequest if config.TRUSTED_HOSTS else flask.Request

app.jinja_env.line_statement_prefix = '#'
app.jinja_env.line_comment_prefix = '##'
app.jinja_env.globals.update(
  check_form_fields=util.check_form_fields,
  datetime=datetime,
  is_iterable=util.is_iterable,
  slugify=util.slugify,
  update_query_argument=util.update_query_argument,
)


white = ['http://localhost:', 'https://excalidraw.com', 'excalidraw-team.now.sh', 'excalidraw.now.sh', 'https://dai-shi.github.io']


@app.after_request
def add_cors_headers(response):
    origin = flask.request.environ['HTTP_ORIGIN'] if 'HTTP_ORIGIN' in flask.request.environ else None
    if not origin:
      return response
    for url in white:
      if url in origin:
        parsed_uri = urlparse(origin)
        result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        response.headers.add('Access-Control-Allow-Origin', result[:-1])
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
        response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
        response.headers.add('Access-Control-Allow-Headers', 'Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        break
    return response


import auth
import control
import model
import task

from api import helpers
api_v1 = helpers.Api(app, prefix='/api/v1')
api_v2 = helpers.Api(app, prefix='/api/v2')
import api.v1
import api.v2

if config.DEVELOPMENT:
  from werkzeug import debug
  try:
    app.wsgi_app = debug.DebuggedApplication(
      app.wsgi_app, evalex=True, pin_security=False,
    )
  except TypeError:
    app.wsgi_app = debug.DebuggedApplication(app.wsgi_app, evalex=True)
  app.testing = False
