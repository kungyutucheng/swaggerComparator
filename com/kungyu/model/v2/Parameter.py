# -*- coding: UTF-8 -*-
import sys
sys.path.append('..')
from model.base.Parameter import Parameter
from model.base.BaseParameter import BaseParameter

reload(sys)
sys.setdefaultencoding('utf8')


class Parameter(Parameter, BaseParameter):
    # in_ 为body的情况下
    schema = None
    # in_为其他的情况下,使用BaseParameter的属性
    allow_empty_value = None
