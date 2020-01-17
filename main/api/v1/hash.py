# coding: utf-8

from __future__ import absolute_import

import json
import hashlib
import flask
import flask_restful
from flask_restful import reqparse

from api import helpers
import model

from main import api_v1

parser = reqparse.RequestParser()
parser.add_argument('json')


@api_v1.resource('/post/', endpoint='api.create')
class DrawingCreateAPI(flask_restful.Resource):
  def post(self):
    try:
      drawing_json = json.loads(flask.request.data)
      m = hashlib.md5()
      m.update(str(drawing_json))
      drawing_hash = m.hexdigest()
      drawing_db = model.Drawing.get_by('hash', drawing_hash)
      if not drawing_db:
        drawing_db = model.Drawing(hash=drawing_hash, json=drawing_json)
      drawing_db.put()
    except (ValueError, AssertionError):
      helpers.make_not_found_exception('Not valid JSON')

    return flask.jsonify({
      'json': flask.url_for('api.hash', drawing_hash=drawing_hash, _external=True)
    })


@api_v1.resource('/<string:drawing_hash>.json', endpoint='api.hash')
class DrawingHashAPI(flask_restful.Resource):
  def get(self, drawing_hash):
    drawing_db = model.Drawing.get_by('hash', drawing_hash)
    if not drawing_db:
      helpers.make_not_found_exception('Drawing %s not found' % drawing_hash)
    return flask.jsonify(drawing_db.json)
