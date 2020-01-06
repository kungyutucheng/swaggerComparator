# -*- coding: UTF-8 -*-
import sys
from com.kungyu.model.base.Operation import Operation

reload(sys)
sys.setdefaultencoding('utf8')


class Operation(Operation):

    consumes = []
    produces = []
    schemas = []