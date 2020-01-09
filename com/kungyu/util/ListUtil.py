# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class ListUtil(object):

    @staticmethod
    def joinList(list, sep):
        str = reduce(lambda v1, v2: v1 + v2, map(lambda v: v + sep, list))
        return str[:len(str) - 1]