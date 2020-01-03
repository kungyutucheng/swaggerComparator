# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class Operation(object):

    tags = None
    summary = None
    description = None
    external_docs = None
    operation_id = None
    parameters = {}
    responses = {}
    deprecated = None
    security = None