#-*- coding: UTF-8 -*-
import os
import sys
import re
import requests
import json
import platform
import getpass
from Downloader import Downloader
from Parser import Parser
from Diff import Diff


class SwaggerComparator(object):

    def __init__(self):
        self.downloader = Downloader()

    def diff(self,new_url,orig_url):
        new_response = requests.request("get", new_url)
        new_json = json.loads(new_response.content)
        self.parser = Parser(new_json)
        new_api_dict = self.parser.parse()

        orig_response = requests.request("get", orig_url)
        orig_json = json.loads(orig_response.content)
        self.parser = Parser(orig_json)
        orig_api_dict = self.parser.parse()

        diff = Diff(new_api_dict, orig_api_dict)
        diff_property_list = diff.diff()

        html = '<html>'
        html += '<head>'
        html += '<title>swaager接口对比差异文件</title>'
        html += '<style>'
        html += 'table, td, th'
        html += '{'
        html += 'border:1px solid black;'
        html += 'border-radius: 2px;'
        html += '}'
        html += 'td'
        html += '{'
        html += 'padding:10px;'
        html += '}'
        html += 'table tr th{'
        html += 'background: #ffd;'
        html += '}'
        html += 'table tr:nth-child(odd){'
        html += 'background: #F5F5F5;'
        html += '}	'
        html += 'table tr:nth-child(even){'
        html += 'background: #efe;'
        html += '}	'
        html += '</style>'
        html += '<body>'
        html += '<p>当前版本：' + new_url + '</p><br/>'
        html += '<p>对比版本：' + orig_url + '</p><br/>'
        html += '<table><tr>'
        html += '<th>接口url</th>'
        html += '<th>method</th>'
        html += '<th>改动类型</th>'
        html += '<th>旧值</th>'
        html += '<th>新值</th>'
        html += '<th>字段名称</th>'
        for diff_property in diff_property_list:
            html += diff_property.to_tr_html()
        html += '</tr></table>'

        html += '</body>'
        html += '</html>'

        os_type = platform.platform().lower()
        user_name = getpass.getuser()
        base_dir = None
        parent_dir = os.sep + 'swagger-html' + os.sep
        file_name = 'swagger_diff.html'
        if os_type.startswith('darwin'):
            base_dir = os.sep + 'Users' + os.sep + user_name + parent_dir
        elif os_type.startswith('linux') or os_type.startswith('unix'):
            base_dir = os.sep + 'usr' + os.sep + 'local' + os.sep + user_name + parent_dir
        else:
            base_dir = 'C:' + os.sep + 'Users' + os.sep + user_name + parent_dir

        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        html_file = open(base_dir + os.sep + file_name, 'w+')
        html_file.write(html)
        html_file.close()





        
if __name__ == '__main__':
    
    argvs = sys.argv
    if len(argvs) != 4:
        print "illegal number of arguments"
        exit(0)

    command = argvs[1]
    if command == "diff":
        new_url = argvs[2]
        orig_url = argvs[3]
        if not re.match(r'^https?:/{2}\w.+$',new_url):
            print "first url is illegal"
            exit(0)

        if not re.match(r'^https?:/{2}\w.+$',orig_url):
            print "second url is illegal"
            exit(0)

        swaggerComparator = SwaggerComparator()
        swaggerComparator.diff(new_url, orig_url)
    else:
        print "invalid command"
        exit(0)
