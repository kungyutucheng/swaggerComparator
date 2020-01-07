# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class SecuritySchema(object):
    type = None
    description = None
    name = None
    in_ = None
    schema = None
    bearer_format= None
    flows = []
    open_id_connect_url = None