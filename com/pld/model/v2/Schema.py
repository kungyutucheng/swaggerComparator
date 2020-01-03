# -*- coding: UTF-8 -*-
import sys
from com.pld.model.base.Schema import Schema

reload(sys)
sys.setdefaultencoding('utf8')


class Schema(Schema):

    ref = None
    description = None
    discriminator = None