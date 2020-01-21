# coding: utf-8

import flask

import auth
import model
import util

from main import app


###############################################################################
# Admin List
###############################################################################
@app.route('/admin/drawing/')
@auth.admin_required
def admin_drawing_list():
  drawing_dbs, drawing_cursor = model.Drawing.get_dbs(
    order=util.param('order') or '-modified',
  )
  return flask.render_template(
    'drawing/admin_drawing_list.html',
    html_class='admin-drawing-list',
    title='Drawing List',
    drawing_dbs=drawing_dbs,
    next_url=util.generate_next_url(drawing_cursor),
    api_url=flask.url_for('api.admin.drawing.list'),
  )
