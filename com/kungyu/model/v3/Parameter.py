# -*- coding: UTF-8 -*-
import sys
from com.kungyu.model.base.Parameter import Parameter
from com.kungyu.model.base.BaseParameter import BaseParameter

reload(sys)
sys.setdefaultencoding('utf8')


class Parameter(Parameter, BaseParameter):
    deprecated = None
    allow_empty_value = None
    style = None
    explode = None
    allow_reserved = None
    schema = None
    example = None
    examples = {}
    content = {}