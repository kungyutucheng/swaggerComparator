# -*- coding: UTF-8 -*-
import sys
from com.kungyu.model.base.Response import Response

reload(sys)
sys.setdefaultencoding('utf8')


class Response(Response):
    schema = None
    examples = {}