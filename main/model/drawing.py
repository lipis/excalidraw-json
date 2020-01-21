# coding: utf-8

from __future__ import absolute_import

import json
from google.appengine.ext import ndb

from api import fields
import model
import util


class Drawing(model.Base):
  hash = ndb.StringProperty(required=True)
  json = ndb.JsonProperty(required=True, compressed=True, verbose_name=u'JSON')

  @ndb.ComputedProperty
  def size(self):
    if self.json:
      return len(json.dumps(self.json))
    return 0

  FIELDS = {
    'hash': fields.String,
    'json': fields.Raw,
  }

  FIELDS.update(model.Base.FIELDS)
