# coding: utf-8

from __future__ import absolute_import

import json
from google.appengine.ext import ndb

from api import fields
import model


class Drawing(model.Base):
  json = ndb.JsonProperty(compressed=True, verbose_name=u'JSON')
  data = ndb.BlobProperty(compressed=True)

  @ndb.ComputedProperty
  def size(self):
    if self.json:
      return len(json.dumps(self.json))
    if self.data:
      return len(self.data)
    return 0

  @ndb.ComputedProperty
  def elements(self):
    if self.json and 'elements' in self.json:
      return len(self.json['elements'])
    return 0

  FIELDS = {
    'json': fields.Raw,
    'size': fields.Integer,
    'elements': fields.Integer,
  }

  FIELDS.update(model.Base.FIELDS)
