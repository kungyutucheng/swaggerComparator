# -*- coding: UTF-8 -*-
import sys
sys.path.append('..')
from model.base.PathItem import PathItem

reload(sys)
sys.setdefaultencoding('utf8')


class PathItem(PathItem):

    parameters = {}
    summary = None
    description = None
    servers = []