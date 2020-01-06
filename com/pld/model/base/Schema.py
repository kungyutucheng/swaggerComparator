# -*- coding: UTF-8 -*-
import sys
from BaseParameter import BaseParameter

reload(sys)
sys.setdefaultencoding('utf8')


class Schema(BaseParameter):
    title = None
    all_of = None
    properties = None
    additional_properties = None
    read_only = None
    xml = None
    external_docs = None
    example = None