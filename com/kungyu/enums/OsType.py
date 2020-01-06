# -*- coding: UTF-8 -*-
import sys
from enum import Enum

reload(sys)
sys.setdefaultencoding('utf8')


class OsType(Enum):

    MAC = "mac"
    LINUX = "linux"
    WINDOWS = "windows"
