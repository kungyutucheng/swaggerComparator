# -*- coding: UTF-8 -*-


class Method(object):
    def __init__(self, method, summary, request, response, tags, consumes, produces):
        self.summary = summary
        self.request = request
        self.response = response
        self.method = method
        self.tags = tags
        self.consumes = consumes
        self.produces = produces