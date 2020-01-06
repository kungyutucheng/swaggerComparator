# -*- coding: UTF-8 -*-
class Request(object):
    def __init__(self, name, required, type, description, properties):
        self.name = name
        self.required = required
        self.type = type
        self.description = description
        self.properties = properties
