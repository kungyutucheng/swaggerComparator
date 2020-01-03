# -*- coding: UTF-8 -*-
import sys
from com.pld.model.base.Operation import Operation

reload(sys)
sys.setdefaultencoding('utf8')


class Operation(Operation):

    request_body = {}
    callbacks = {}
    servers = []