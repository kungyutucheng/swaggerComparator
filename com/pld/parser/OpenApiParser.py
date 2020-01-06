# -*- coding: UTF-8 -*-
import sys
from Parser import Parser

reload(sys)
sys.setdefaultencoding('utf8')


class OpenApiParser(Parser):

    def __init__(self, json):
        self.json = json

    def parse(self):
        pass