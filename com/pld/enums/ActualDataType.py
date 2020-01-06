# -*- coding: UTF-8 -*-
import sys
from enum import Enum

reload(sys)
sys.setdefaultencoding('utf8')


class ActualDataType(Enum):
    integer = "integer"
    long = "long"
    float = "float"
    double = "double"
    string = "string"
    byte = "byte"
    binary = "binary"
    boolean = "boolean"
    date = "date"
    dateTime = "dateTime"
    password = "password"