# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class Response(object):
    content = {}
    links = {}
    description = None
    headers = {}