# -*- coding: UTF-8 -*-
import sys
from com.pld.model.Response import Response

reload(sys)
sys.setdefaultencoding('utf8')


class Response(Response):
    content = {}
    links = {}