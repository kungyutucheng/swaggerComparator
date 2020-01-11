# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class ListUtil(object):

    @staticmethod
    def joinList(list, sep):
        result = reduce(lambda v1, v2: str(v1) + str(v2), map(lambda v: str(v) + sep, list))
        return result[:len(result) - 1]