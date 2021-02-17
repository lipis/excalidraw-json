# coding: utf-8

from __future__ import absolute_import

import json
import flask
import flask_restful

from api import helpers
import model
import task

from main import api_v1


@api_v1.resource('/post/', endpoint='api.create')
class DrawingCreateAPI(flask_restful.Resource):
  def post(self):
    try:
      drawing_json = json.loads(json.dumps(json.loads(flask.request.data), indent=2, sort_keys=True))
      drawing_db = model.Drawing(json=drawing_json)
      drawing_db.put()
      task.task_calculate_stats(drawing_db.created)
    except (ValueError, AssertionError):
      helpers.make_not_found_exception('Not valid JSON')

    response = flask.make_response(flask.jsonify({
      'id': drawing_db.key.id(),
      'json': flask.url_for('api.id', drawing_id=drawing_db.key.id(), _external=True),
    }))
    return response


@api_v1.resource('/<int:drawing_id>.json', endpoint='api.id')
class DrawingHashAPI(flask_restful.Resource):
  def get(self, drawing_id):
    drawing_db = model.Drawing.get_by_id(drawing_id)
    if not drawing_db or not drawing_db.json:
      helpers.make_not_found_exception('Drawing %s not found' % drawing_id)
    if drawing_db.json:
      return flask.jsonify(drawing_db.json)
