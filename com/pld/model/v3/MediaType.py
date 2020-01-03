# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class MediaType(object):
    schema = None
    example = None
    examples = {}
    encoding = {}
