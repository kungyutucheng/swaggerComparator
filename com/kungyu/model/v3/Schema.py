# -*- coding: UTF-8 -*-
import sys
from com.kungyu.model.base.Schema import Schema

reload(sys)
sys.setdefaultencoding('utf8')


class Schema(Schema):
    discriminator = None
    write_only = None
    deprecated = None
    any_of = {}
    one_of = {}
    not_ = {}