# -*- coding: UTF-8 -*-
import requests
import json
import os
import webbrowser
from com.kungyu.enums.DiffType import DiffType
from com.kungyu.model.DiffProperty import DiffProperty
from com.kungyu.enums.PropertyType import PropertyType
from Command import Command
from Parser import Parser
from com.kungyu.util.SystemUtil import SystemUtil
from com.kungyu.util.HtmlGenerator import HtmlGenerator



class Diff(Command):
    def __init__(self, new_url, orig_url, dest_directory=SystemUtil.get_sys_user_path('swagger-html'), file_name='swagger-diff.html'):
        self.new_api_dict = None
        self.orig_api_dict = None
        self.new_url = new_url
        self.orig_url = orig_url
        self.dest_directory = dest_directory
        self.file_name = file_name
        self.diff_list = []

    def execute(self):
        # request the new_url and orig_url to get response json
        new_response = requests.request("get", self.new_url)
        new_json = json.loads(new_response.content)
        orig_response = requests.request("get", self.orig_url)
        orig_json = json.loads(orig_response.content)

        # parse the response json of new_url and orig_url
        parser = Parser(new_json)
        self.new_api_dict = parser.parse()
        parser = Parser(orig_json)
        self.orig_api_dict = parser.parse()

        # to generate the diff_list
        self.diff()

        # to generate the result html file
        if self.dest_directory is None:
            self.dest_directory = SystemUtil.get_sys_user_path('swagger-html')
        if not os.path.isdir(self.dest_directory):
            os.mkdir(self.dest_directory)
        html_content = HtmlGenerator.generate_diff_html(self.new_url, self.orig_url, self.diff_list)
        path = self.dest_directory + os.sep + self.file_name
        html_file = open(path, 'w+')
        html_file.write(html_content)
        html_file.close()

        # open html file using default web browser
        webbrowser.open_new_tab('file:' + os.sep + os.sep + path)

    def diff(self):
        self.diff_path()
        return self.diff_list

    def diff_path(self):
        for new_api_path in self.new_api_dict:
            flag = False
            fist_method_dict = self.new_api_dict.get(new_api_path).methods
            if new_api_path in self.orig_api_dict:
                orig_method_dict = self.orig_api_dict.get(new_api_path).methods
                self.diff_method(new_api_path, fist_method_dict, orig_method_dict)
                flag = True
            if not flag:
                self.diff_method(new_api_path, fist_method_dict, {})
        for orig_api_path in self.orig_api_dict:
            orig_method_dict = self.orig_api_dict.get(orig_api_path).methods
            if orig_api_path not in self.new_api_dict:
                self.diff_method(orig_api_path, {}, orig_method_dict)

    # 对比不同的method，比如说新增了post，或者删除了get
    def diff_method(self, path, new_method_dict, orig_method_dict):
        for new_method in new_method_dict:
            # method 新增
            if new_method not in orig_method_dict:
                self.build_method_diff(path, new_method, DiffType.API_METHOD_ADD, new_method, None)
            else:
                self.diff_method_detail(path, new_method, new_method_dict[new_method], orig_method_dict[new_method])
        for orig_method in orig_method_dict:
            # method 删除
            if orig_method not in new_method_dict:
                self.build_method_diff(path, orig_method, DiffType.API_METHOD_DELETE, None, orig_method)

    def build_method_diff(self, path, method, diff_type, new_method, orig_method):
        if diff_type == DiffType.API_METHOD_ADD:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_method, None))
        elif diff_type == DiffType.API_METHOD_DELETE:
            self.diff_list.append(DiffProperty(path, method, diff_type, None, orig_method))
        elif diff_type == DiffType.API_METHOD_MODIFY_SUMMARY:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_method.summary, orig_method.summary))
        elif diff_type == DiffType.API_METHOD_MODIFY_TAGS:
            self.diff_list.append(DiffType(path, method, diff_type, new_method.tags, orig_method.tags))
        elif diff_type == DiffType.API_METHOD_MODIFY_CONSUMES:
            self.diff_list.append(DiffType(path, method, diff_type, new_method.consumes, orig_method.consums))
        elif diff_type == DiffType.API_METHOD_MODIFY_PRODUCES:
            self.diff_list.append(DiffType(path, method, diff_type, new_method.produces, orig_method.produces))

    # 对比method内的具体属性
    def diff_method_detail(self, path, method, new_method, orig_method):
        if new_method.summary != orig_method.summary:
            self.build_method_diff(path, method, DiffType.API_METHOD_MODIFY_SUMMARY, new_method, orig_method)
        if new_method.tags != orig_method.tags:
            self.build_method_diff(path, method, DiffType.API_METHOD_MODIFY_TAGS, new_method, orig_method)
        if new_method.consumes != orig_method.consumes:
            self.build_method_diff(path, method, DiffType.API_METHOD_MODIFY_CONSUMES, new_method.consumes, orig_method.consumes)
        if new_method.produces != orig_method.produces:
            self.build_method_diff(path, method, DiffType.API_METHOD_MODIFY_PRODUCES, new_method.produces, orig_method.produces)
        self.diff_request(path, method, new_method.request, orig_method.request)
        self.diff_response(path, method, new_method.response, orig_method.response)

    # 对比request
    def diff_request(self, path, method, new_request_list, orig_request_list):
        if new_request_list is not None:
            for new_request in new_request_list:
                flag = False
                for orig_request in orig_request_list:
                    if new_request.name == orig_request.name:
                        flag = True
                        # 俩者均存在的字段比较实体的属性
                        self.diff_request_detail(path, method, new_request, orig_request)
                # 新增的字段
                if not flag:
                    self.build_request_diff(path, method, DiffType.REQUEST_PARAMETER_ADD, new_request, None)
        if orig_request_list is not None:
            for orig_request in orig_request_list:
                flag = False
                if new_request_list is not None:
                    for new_request in new_request_list:
                        if new_request.name == orig_request.name:
                            flag = True
                # 新增的字段
                if not flag:
                    self.build_request_diff(path, method, DiffType.REQUEST_PARAMETER_DELETE, None, orig_request)

    def build_request_diff(self, path, method, diff_type, new_request, orig_request):
        if diff_type == DiffType.REQUEST_PARAMETER_ADD:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_request.name, None))
        if diff_type == DiffType.REQUEST_PARAMETER_DELETE:
            self.diff_list.append(DiffProperty(path, method, diff_type, None, orig_request.name))
        if diff_type == DiffType.REQUEST_PARAMETER_MODIFY_TYPE:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_request.type, orig_request.type, orig_request.name))
        if diff_type == DiffType.REQUEST_PARAMETER_MODIFY_DESC:
            self.diff_list.append(
                DiffProperty(path, method, diff_type, new_request.description, orig_request.description, orig_request.name))
        if diff_type == DiffType.RESPONSE_PARAMETER_MODIFY_REQUIRED:
            self.diff_list.append(
                DiffProperty(path, method, diff_type, new_request.required, orig_request.required, orig_request.name))
        if diff_type == DiffType.REQUEST_PARAMETER_MODIFY_REF:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_request.ref, orig_request.ref, orig_request.name))

    # 对比response
    def diff_response(self, path, method, new_response, orig_response):
        if new_response is None and orig_response is not None:
            self.diff_list.append(DiffProperty(path, method, DiffType.RESPONSE_PARAMETER_DELETE, None, None))
        if new_response is not None and orig_response is None:
            self.diff_list.append(DiffProperty(path, method, DiffType.RESPONSE_PARAMETER_ADD, None, None))
        if new_response is not None and orig_response is not None:
            if new_response.type != orig_response.type:
                self.diff_list.append(
                    DiffProperty(path, method, DiffType.RESPONSE_PARAMETER_MODIFY_TYPE, new_response.type, orig_response.type))
            self.diff_property(path, method, new_response.properties, orig_response.properties, PropertyType.RESPONSE)

    # 对比每个method对应的request的属性，比如说post对应的request的必填/类型这些属性，是request外层大属性，property才是真正的字段
    def diff_request_detail(self, path, method, new_request, orig_request):
        diff_type = None
        if new_request.required != orig_request.required:
            diff_type = DiffType.REQUEST_PARAMETER_MODIFY_REQUIRED
        if new_request.type != orig_request.type:
            diff_type = DiffType.REQUEST_PARAMETER_MODIFY_TYPE
        if new_request.description != orig_request.description:
            diff_type = DiffType.REQUEST_PARAMETER_MODIFY_DESC
        if diff_type:
            self.build_request_diff(path, method, diff_type, new_request, orig_request)
        else:
            # 对比实体字段
            self.diff_property(path, method, new_request.properties, orig_request.properties, PropertyType.REQUEST)

    # 对比属性，由于property 在request和response中共用，所以使用property_type来区分
    def diff_property(self, path, method, new_properties, orig_properties, property_type):
        if new_properties is not None:
            for new_property in new_properties:
                flag = False
                if orig_properties is not None:
                    for orig_property in orig_properties:
                        if new_property.name == orig_property.name:
                            flag = True
                            # 对比实体字段的其他属性
                            self.diff_property_detail(path, method, new_property, orig_property, property_type)
                if not flag:
                    self.build_property_diff(path, method, DiffType.get_diff_type(property_type, 'PARAMETER_ADD'), new_property,
                                             None)
        if orig_properties is not None:
            for orig_property in orig_properties:
                flag = False
                if new_properties is not None:
                    for new_property in new_properties:
                        if new_property.name == orig_property.name:
                            flag = True
                if not flag:
                    self.build_property_diff(path, method, DiffType.get_diff_type(property_type, 'PARAMETER_DELETE'), None,
                                             orig_property)

    def build_property_diff(self, path, method, diff_type, new_property, orig_property):
        if diff_type == DiffType.REQUEST_PARAMETER_ADD or diff_type == DiffType.RESPONSE_PARAMETER_ADD:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_property.name, None))
        if diff_type == DiffType.REQUEST_PARAMETER_DELETE or diff_type == DiffType.RESPONSE_PARAMETER_DELETE:
            self.diff_list.append(DiffProperty(path, method, diff_type, None, orig_property.name))
        if diff_type == DiffType.REQUEST_PARAMETER_MODIFY_REQUIRED or diff_type == DiffType.RESPONSE_PARAMETER_MODIFY_REQUIRED:
            self.diff_list.append(
                DiffProperty(path, method, diff_type, new_property.required, orig_property.required, orig_property.name))
        if diff_type == DiffType.REQUEST_PARAMETER_MODIFY_DESC or diff_type == DiffType.RESPONSE_PARAMETER_MODIFY_DESC:
            self.diff_list.append(
                DiffProperty(path, method, diff_type, new_property.description, orig_property.description, orig_property.name))
        if diff_type == DiffType.REQUEST_PARAMETER_MODIFY_TYPE or diff_type == DiffType.RESPONSE_PARAMETER_MODIFY_TYPE:
            self.diff_list.append(
                DiffProperty(path, method, diff_type, new_property.type, orig_property.type, orig_property.name))
        if diff_type == DiffType.REQUEST_PARAMETER_MODIFY_REF or diff_type == DiffType.RESPONSE_PARAMETER_MODIFY_REF:
            self.diff_list.append(
                DiffProperty(path, method, diff_type, new_property.ref, orig_property.ref, orig_property.name))

    # 对比property具体属性
    def diff_property_detail(self, path, method, new_property, orig_property, property_type):
        suffix = None
        if new_property.type != orig_property.type:
            suffix = 'PARAMETER_MODIFY_TYPE'
        if new_property.description != orig_property.description:
            suffix = 'PARAMETER_MODIFY_DESC'
        if new_property.required != orig_property.required:
            suffix = 'PARAMETER_MODIFY_REQUIRED'
        if new_property.ref != orig_property.ref:
            suffix = 'PARAMETER_MODIFY_REF'
        if suffix:
            diff_type = DiffType.get_diff_type(property_type, suffix)
            self.build_property_diff(path, method, diff_type, new_property, orig_property)
        # 递归对比items
        self.diff_property(path, method, new_property.items, orig_property.items, property_type)
