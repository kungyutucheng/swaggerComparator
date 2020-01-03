# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class OpenApi(object):
    """
    swagger v3.x root
    """
    open_api = None
    info = None
    servers = []
    paths = {}
    components = None
    security = []
    tags = []
    external_docs = None