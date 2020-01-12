# -*- coding: UTF-8 -*-
import sys
sys.path.append('..')
from model.base.Response import Response

reload(sys)
sys.setdefaultencoding('utf8')


class Response(Response):
    schema = None
    examples = {}