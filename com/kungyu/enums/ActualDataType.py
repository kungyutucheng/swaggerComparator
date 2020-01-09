# -*- coding: UTF-8 -*-
import sys
from enum import Enum

reload(sys)
sys.setdefaultencoding('utf8')


class ActualDataType(Enum):
    INTEGER = 'integer'
    LONG = 'long'
    FLOAT = 'float'
    DOUBLE = 'double'
    STRING = 'string'
    BYTE = 'byte'
    BINARY = 'binary'
    BOOLEAN = 'boolean'
    DATE = 'date'
    DATE_TIME = 'dateTime'
    PASSWORD = 'password'