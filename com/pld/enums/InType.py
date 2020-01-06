# -*- coding: UTF-8 -*-
import sys
from enum import Enum

reload(sys)
sys.setdefaultencoding('utf8')


class InType(Enum):

    PATH = 'path'
    QUERY = 'query'
    header = 'header'
    BODY = 'body'