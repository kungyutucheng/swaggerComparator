# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class Component(object):

    """
    swagger v3.x
    """
    schemas = {}
    responses = {}
    parameters = {}
    examples = {}
    request_bodies = {}
    headers = {}
    security_schemes = {}
    links = {}
    callbacks = {}
