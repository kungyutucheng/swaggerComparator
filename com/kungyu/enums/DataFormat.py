# -*- coding: UTF-8 -*-
import sys
from enum import Enum

reload(sys)
sys.setdefaultencoding('utf8')


class DataFormat(Enum):
    INT32 = 'int32'
    INT64 = 'int64'
    FLOAT = 'float'
    DOUBLE = 'double'
    BYTE = 'byte'
    BINARY = 'binary'
    DATE = 'date'
    DATE_TIME = 'date-time'
    PASSWORD = 'password'