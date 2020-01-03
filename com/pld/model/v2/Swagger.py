# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


# swagger 2.0 version root
class Swagger(object):
    swagger = None
    info = None
    host = None
    base_path = None
    schemes = []
    consumes = []
    produces = []
    paths = {}
    definitions = {}
    parameters = []
    responses = {}
    security_definitions = {}
    security = {}
    tags = []
    external_docs = None
