# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class Link(object):
    operation_ref = None
    operation_id = None
    parameters = {}
    request_body = None
    description = None
    server = None