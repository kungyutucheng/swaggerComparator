# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class BaseParameter(object):
    type = None
    format = None
    items = None
    collection_format = None
    default = None
    maximum = None
    exclusive_maximum = None
    minimum = None
    exclusive_minimum = None
    max_length = None
    min_length = None
    pattern = None
    max_items = None
    min_items = None
    unique_items = None
    enum = None
    multiple_of = None