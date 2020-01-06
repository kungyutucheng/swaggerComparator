# -*- coding: UTF-8 -*-
import sys
from enum import Enum

reload(sys)
sys.setdefaultencoding('utf8')


class DataFormat(Enum):
    int32 = "int32"
    int64 = "int64"
    float = "float"
    double = "double"
    byte = "byte"
    binary = "binary"
    date = "date"
    date_time = "date-time"
    password = "password"