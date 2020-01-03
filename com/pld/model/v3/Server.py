# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class Server(object):
    """
    swagger v3.x
    """
    url = None
    description = None
    variables = {}