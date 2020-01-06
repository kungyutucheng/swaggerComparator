# -*- coding: UTF-8 -*-
import sys
from enum import Enum

reload(sys)
sys.setdefaultencoding('utf8')


class ShowDataType(Enum):
    integer = "integer"
    number = "number"
    string = "string"
    boolean = "boolean"