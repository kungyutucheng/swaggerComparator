# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class OAuthFlow(object):
    authorization_url = None
    token_url = None
    refresh_url = None
    scopes = {}