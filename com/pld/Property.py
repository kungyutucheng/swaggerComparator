# -*- coding: UTF-8 -*-


class Property(object):

    def __init__(self, name, type, description, required, items, ref):
        self.name = name
        self.type = type
        self.description = description
        self.required = required
        self.items = items
        self.ref = ref
