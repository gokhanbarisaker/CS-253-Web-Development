# -*- coding: UTF-8 -*-

import webapp2
import security
from models.user import User

# Returns user instance if given request has valid credentials,
# Otherwise, None.
#
def authenticate(request):
    user = None
    user_hash = request.cookies.get('user')
    user_id = security.validate_hash(user_hash)

    if user_id:
      user = User.get_by_id(long(user_id))

    return user
