# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class Tag(object):
    name = None
    description = None
    external_docs = None