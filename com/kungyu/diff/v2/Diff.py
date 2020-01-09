# -*- coding: UTF-8 -*-
import sys
import requests
import json
from com.kungyu.diff.Command import Command
from com.kungyu.util.SystemUtil import SystemUtil
from com.kungyu.parser.SwaggerParser import SwaggerParser
from com.kungyu.parser.OpenApiParser import OpenApiParser
from SwaggerDiff import SwaggerDiff

reload(sys)
sys.setdefaultencoding('utf8')


class Diff(Command):

    def __init__(self, new_url, orig_url, dest_directory=SystemUtil.get_sys_user_path('swagger-ui.html'),file_name='swagger-diff.html'):
        self.new_api_dict = None
        self.orig_api_dict = None
        self.new_url = new_url
        self.orig_url = orig_url
        self.dest_directory = dest_directory
        self.file_name = file_name
        self.diff_list = []

    def execute(self):
        new_response = requests.request('get', self.new_url)
        new_json = json.loads(new_response.content)
        orig_response = requests.request('get', self.orig_url)
        orig_json = json.loads(orig_response.content)

        if 'swagger' in new_json and 'swagger' in orig_json:
            new_parser = SwaggerParser(new_json)
            new_swagger = new_parser.parse()
            orig_parser = SwaggerParser(orig_json)
            orig_swagger = orig_parser.parse()
            swagger_diff = SwaggerDiff(self.new_url, self.orig_url, new_swagger, orig_swagger, self.dest_directory, self.file_name)
            swagger_diff.execute()
        elif 'openapi' in new_json and 'openapi' in orig_json:
            pass
        else:
            print('cannot generate result based on different versions of swagger api')


if __name__ == '__main__':

    diff = Diff('http://localhost:9003/v2/api-docs','http://localhost:9002/v2/api-docs')
    diff.execute()
