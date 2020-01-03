# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class RequestBody(object):
    description = None
    content = {}
    required = None