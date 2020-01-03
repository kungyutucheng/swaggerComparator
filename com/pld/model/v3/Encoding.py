# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class Encoding(object):
    content_type = None
    headers = {}
    style = None
    explode = None
    allow_reserved = None