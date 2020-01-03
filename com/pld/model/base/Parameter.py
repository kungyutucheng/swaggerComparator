# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class Parameter(object):
    name = None
    in_ = None
    description = None
    required = None