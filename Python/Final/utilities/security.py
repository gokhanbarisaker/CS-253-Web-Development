# -*- coding: UTF-8 -*-

import hashlib
import hmac

Secret = "ShBNcNprEAx5ZMHPuNJ8YajSpmeHT59b"

def generate_salt(length = 5):
  return ''.join(random.choice(string.letters) for x in xrange(length))

def generate_hash(data):
  h = hashlib.sha256(data).hexdigest()
  return '{0}|{1}'.format(h, data)

def generate_hmac(data, key = Secret, salt = None):
  if not salt:
    salt = make_salt()
  h = hmac.new(key, data, salt)
  return '{0}|{1}'.format(h, salt)

def validate_hash(h):
  if isinstance(h, basestring):
    data = h.split('|')[-1]

    if generate_hash(data) == h:
      return data
