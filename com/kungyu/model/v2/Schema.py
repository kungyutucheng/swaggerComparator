# -*- coding: UTF-8 -*-
import sys
from com.kungyu.model.base.Schema import Schema

reload(sys)
sys.setdefaultencoding('utf8')


class Schema(Schema):

    ref = None
    description = None
    discriminator = None
    required = None