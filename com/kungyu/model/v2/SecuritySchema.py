# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class SecuritySchema(object):
    type = None
    description = None
    name = None
    in_ = None
    flow = None
    authorization_url = None
    token_url = None
    scopes = None