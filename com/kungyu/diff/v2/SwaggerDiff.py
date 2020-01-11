# -*- coding: UTF-8 -*-
import sys
import os
import webbrowser
from com.kungyu.diff.Command import Command
from com.kungyu.util.SystemUtil import SystemUtil
from com.kungyu.util.HtmlGenerator import HtmlGenerator
from com.kungyu.enums.DiffType import DiffType
from com.kungyu.model.DiffProperty import DiffProperty
from com.kungyu.util.TypeConvertor import TypeConvertor
from com.kungyu.enums.PropertyType import PropertyType
from com.kungyu.enums.ShowDataType import ShowDataType

reload(sys)
sys.setdefaultencoding('utf8')


class SwaggerDiff(Command):

    def __init__(self, new_url, orig_url, new_swagger, orig_swagger, dest_directory, file_name):
        self.new_url = new_url
        self.orig_url = orig_url
        self.new_swagger = new_swagger
        self.orig_swagger = orig_swagger
        self.dest_directory = dest_directory
        self.file_name = file_name
        self.diff_list = []

    def execute(self):
        self.diff()

        if self.dest_directory is None:
            self.dest_directory = SystemUtil.get_sys_user_path('swagger-html')
        if not os.path.isdir(self.dest_directory):
            os.mkdir(self.dest_directory)
        html_content = HtmlGenerator.generate_diff_html(self.new_url, self.orig_url, self.diff_list)
        path = self.dest_directory + os.sep + self.file_name
        html_file = open(path, 'w+')
        html_file.write(html_content)
        html_file.close()

        webbrowser.open_new_tab('file:' + os.sep + os.sep + path)

    def diff(self):
        if self.new_swagger.host != self.orig_swagger.host:
            self.diff_list.append(DiffProperty(None, None, DiffType.HOST, self.new_swagger.host, self.orig_swagger.host))
        if self.new_swagger.base_path != self.orig_swagger.base_path:
            self.diff_list.append(DiffProperty(None, None, DiffType.BASE_PATH, self.new_swagger.base_path, self.orig_swagger.base_path))
        self.diff_paths()

    def diff_paths(self):
        # 检测是否有新增接口
        for new_path in self.new_swagger.paths:
            flag = False
            new_operation_map = self.new_swagger.paths.get(new_path).operation_map
            if new_path in self.orig_swagger.paths:
                orig_operation_map = self.orig_swagger.paths.get(new_path).operation_map
                # 原先存在的接口，对method进行对比
                self.diff_operation_map(new_path, new_operation_map, orig_operation_map)
                flag = True
            if not flag:
                # 全新接口，对method全量生成对比数据
                self.diff_operation_map(new_path, new_operation_map, {})
        # 检测是否有删除接口
        for orig_path in self.orig_swagger.paths:
            orig_operation_map = self.orig_swagger.paths.get(orig_path).operation_map
            if orig_path not in self.new_swagger.paths:
                self.diff_operation_map(orig_path, {}, orig_operation_map)

    def diff_operation_map(self, path, new_operation_map, orig_operation_map):
        for new_method in new_operation_map:
            if new_method in orig_operation_map:
                self.diff_operation(path, new_method, new_operation_map.get(new_method), orig_operation_map.get(new_method))
            else:
                self.build_operation_diff(path, new_method, DiffType.API_METHOD_ADD, new_operation_map.get(new_method), None)
        for orig_method in orig_operation_map:
            if orig_method not in new_operation_map:
                self.build_operation_diff(path, orig_method, DiffType.API_METHOD_DELETE, None, orig_operation_map.get(orig_method))

    def diff_operation(self, path, method, new_operation, orig_operation):
        if new_operation.tags != orig_operation.tags:
            self.build_operation_diff(path, method, DiffType.API_METHOD_MODIFY_TAGS, new_operation, orig_operation)
        if new_operation.summary != orig_operation.summary:
            self.build_operation_diff(path, method, DiffType.API_METHOD_MODIFY_SUMMARY, new_operation, orig_operation)
        if new_operation.description != orig_operation.description:
            self.build_operation_diff(path, method, DiffType.API_METHOD_MODIFY_DESCRIPTION, new_operation, orig_operation)
        if new_operation.deprecated != orig_operation.deprecated:
            self.build_operation_diff(path, method, DiffType.API_METHOD_MODIFY_DEPRECATED, new_operation, orig_operation)
        if new_operation.consumes != orig_operation.consumes:
            self.build_operation_diff(path, method, DiffType.API_METHOD_MODIFY_CONSUMES, new_operation, orig_operation)
        if new_operation.produces != orig_operation.produces:
            self.build_operation_diff(path, method, DiffType.API_METHOD_MODIFY_PRODUCES, new_operation, orig_operation)
        self.diff_parameters(path, method, new_operation.summary,  new_operation.parameters, orig_operation.parameters)
        self.diff_responses(path, method, new_operation.summary, new_operation.responses, orig_operation.responses)

    def build_operation_diff(self, path, method, diff_type, new_operation, orig_operation):
        if diff_type == DiffType.API_METHOD_MODIFY_TAGS:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_operation.tags, orig_operation.tags, None, new_operation.summary))
        elif diff_type == DiffType.API_METHOD_MODIFY_SUMMARY:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_operation.summary, orig_operation.summary))
        elif diff_type == DiffType.API_METHOD_MODIFY_DESCRIPTION:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_operation.description, orig_operation.description, None, new_operation.summary))
        elif diff_type == DiffType.API_METHOD_MODIFY_DEPRECATED:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_operation.deprecated, orig_operation.deprecated, None, new_operation.summary))
        elif diff_type == DiffType.API_METHOD_MODIFY_CONSUMES:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_operation.consumes, orig_operation.consumes, None, new_operation.summary))
        elif diff_type == DiffType.API_METHOD_MODIFY_PRODUCES:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_operation.produces, orig_operation.produces, None, new_operation.summary))
        elif diff_type == DiffType.API_METHOD_ADD:
            self.diff_list.append(DiffProperty(path, method, diff_type, method, None, None, new_operation.summary))
        elif diff_type == DiffType.API_METHOD_DELETE:
            self.diff_list.append(DiffProperty(path, method, diff_type, None, method, None, orig_operation.summary))


    def diff_parameters(self, path, method, summary, new_parameters, orig_parameters):
        for new_parameter in new_parameters:
            flag = False
            for orig_parameter in orig_parameters:
                if new_parameter.name == orig_parameter.name:
                    # 对比旧参数
                    self.diff_parameter(path, method, summary, new_parameter, orig_parameter)
                    flag = True
            if not flag:
                # 新增参数
                self.build_parameter_diff(path, method, summary, DiffType.REQUEST_PARAMETER_ADD, new_parameter, None)
        # 删除参数
        for orig_parameter in orig_parameters:
            flag = False
            for new_parameter in new_parameters:
                if orig_parameter.name == new_parameter.name:
                    flag = True
            if not flag:
                self.build_parameter_diff(path, method, summary, DiffType.REQUEST_PARAMETER_DELETE, None, orig_parameter)

    def diff_parameter(self, path, method, summary, new_parameter, orig_parameter):
        if new_parameter.type != orig_parameter.type or new_parameter.format != orig_parameter.format:
            self.build_parameter_diff(path, method, summary, DiffType.REQUEST_PARAMETER_MODIFY_TYPE, new_parameter, orig_parameter)
        if new_parameter.items != orig_parameter.items:
            # todo
            pass
        if new_parameter.required != orig_parameter.required:
            self.build_parameter_diff(path, method, summary, DiffType.REQUEST_PARAMETER_MODIFY_REQUIRED, new_parameter, orig_parameter)
        if new_parameter.description != orig_parameter.description:
            self.build_parameter_diff(path, method, summary, DiffType.REQUEST_PARAMETER_MODIFY_DESC, new_parameter, orig_parameter)
        if new_parameter.schema != orig_parameter.schema:
            self.generate_schema(path, method, summary, new_parameter.schema.ref, orig_parameter.schema.ref, PropertyType.REQUEST)

    def generate_schema(self, path, method, summary, new_ref, orig_ref, property_type):
        new_schema_name = self.generate_ref(new_ref)
        new_schema = self.get_new_definition(new_schema_name)
        orig_schema_name = self.generate_ref(orig_ref)
        orig_schema = self.get_orig_definition(orig_schema_name)
        self.diff_schema(path, method, summary, new_schema, orig_schema, new_schema_name, property_type)

    def build_parameter_diff(self, path, method, summary, diff_type, new_parameter, orig_parameter):
        if diff_type == DiffType.REQUEST_PARAMETER_MODIFY_TYPE:
            self.diff_list.append(DiffProperty(path, method, diff_type, TypeConvertor.convertToActualDataType(new_parameter.type, new_parameter.format), TypeConvertor.convertToActualDataType(orig_parameter.type, orig_parameter.format), new_parameter.field_name, summary))
        if diff_type == DiffType.REQUEST_PARAMETER_MODIFY_REQUIRED:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_parameter.required, orig_parameter.required, new_parameter.name, summary))
        if diff_type == DiffType.REQUEST_PARAMETER_MODIFY_DESC:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_parameter.description, orig_parameter.description, new_parameter.name, summary))
        if diff_type == DiffType.REQUEST_PARAMETER_ADD:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_parameter.name, None, new_parameter.name, summary))
        if diff_type == DiffType.REQUEST_PARAMETER_DELETE:
            self.diff_list.append(DiffProperty(path, method, diff_type, None, orig_parameter.name, orig_parameter.name, summary))
        if diff_type == DiffType.REQUEST_PARAMETER_MODIFY_REF:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_parameter.schema.ref, orig_parameter.schema.ref, new_parameter.name, summary))

    """
    
    """
    def diff_schema(self, path, method, summary, new_schema, orig_schema, new_name, property_type):
        if new_schema is None or orig_schema is None:
            return
        if new_schema.items is not None:
            new_ref = new_schema.items.ref
            orig_ref = orig_schema.items.ref
            # 防止object中的items引用自身造成死循环
            if new_ref != new_name:
                # 对比items内的数据引用
                self.generate_schema(path, method, summary, new_ref, orig_ref, property_type)

        suffix = None
        # 通过type和format综合判断类型是否一致
        if new_schema.type != orig_schema.type or new_schema.format != orig_schema.format:
            suffix = 'schema_modify_type'
            diff_type = DiffType.get_diff_type(property_type, suffix)
            self.build_schema_diff(path, method, summary, diff_type, new_schema, orig_schema, new_name)
        # 判断可选值是否一致
        if new_schema.enum != orig_schema.enum:
            suffix = 'schema_modify_allow_values'
            diff_type = DiffType.get_diff_type(property_type, suffix)
            self.build_schema_diff(path, method, summary, diff_type, new_schema, orig_schema, new_name)
        # 判断只读属性是否一致
        if new_schema.read_only != orig_schema.read_only:
            suffix = 'schema_modify_readonly'
            diff_type = DiffType.get_diff_type(property_type, suffix)
            self.build_schema_diff(path, method, summary, diff_type, new_schema, orig_schema, new_name)
        # 判断object内部属性是否一致
        new_properties = new_schema.properties
        orig_properties = orig_schema.properties
        for new_property_name in new_properties:
            if new_property_name in orig_properties:
                # 对比object类的字段属性
                self.diff_schema(path, method, summary, new_properties.get(new_property_name), orig_properties.get(new_property_name), new_property_name, property_type)
                # 判断必填是否一致，需要在与properties属性同一层判断，因为真正的required与properties是同一层级，如果进入上一句之后在判断，则会丢失required
                new_schema_required = self.generate_schema_required(new_schema.required, new_property_name)
                orig_schema_required = self.generate_schema_required(orig_schema.required, new_property_name)
                if new_schema_required != orig_schema_required:
                    suffix = 'schema_modify_required'
                    diff_type = DiffType.get_diff_type(property_type, suffix)
                    self.build_schema_diff(path, method, summary, diff_type, new_schema, orig_schema, new_property_name)
            else:
                # 新增的字段
                suffix = 'schema_field_add'
                diff_type = DiffType.get_diff_type(property_type, suffix)
                self.build_schema_diff(path, method, summary, diff_type, new_schema, orig_schema, new_property_name)
        for orig_property_name in orig_properties:
            if orig_property_name not in new_properties:
                # 删除字段
                suffix = 'schema_field_delete'
                diff_type = DiffType.get_diff_type(property_type, suffix)
                self.build_schema_diff(path, method, summary, diff_type, new_schema, orig_schema, orig_property_name)
        # 判断描述是否一致
        if new_schema.description != orig_schema.description:
            suffix = 'schema_modify_desc'
            diff_type = DiffType.get_diff_type(property_type, suffix)
            self.build_schema_diff(path, method, summary, diff_type, new_schema, orig_schema, new_name)
        # 判断例子是否一致
        if new_schema.example != orig_schema.example:
            suffix = 'schema_modify_example'
            diff_type = DiffType.get_diff_type(property_type, suffix)
            self.build_schema_diff(path, method, summary, diff_type, new_schema, orig_schema, new_name)


    def generate_ref(self, ref_name):
        if ref_name is None:
            return
        begin_index = ref_name.rfind('/', 0, len(ref_name))
        if begin_index == -1:
            return
        return ref_name[begin_index + 1:]

    def get_new_definition(self, definition_name):
        return self.new_swagger.definitions.get(definition_name)

    def get_orig_definition(self, definition_name):
        return self.orig_swagger.definitions.get(definition_name)

    def build_schema_diff(self, path, method, summary, diff_type, new_schema, orig_schema, field_name):
        if diff_type == DiffType.REQUEST_SCHEMA_MODIFY_TYPE or diff_type == DiffType.RESPONSE_SCHEMA_MODIFY_TYPE:
            self.diff_list.append(DiffProperty(path, method, diff_type, TypeConvertor.convertToActualDataType(new_schema.type, new_schema.format), TypeConvertor.convertToActualDataType(orig_schema.type, orig_schema.format), field_name, summary))
        if diff_type == DiffType.REQUEST_SCHEMA_MODIFY_ALLOW_VALUES or diff_type == DiffType.RESPONSE_SCHEMA_MODIFY_ALLOW_VALUES:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_schema.enum, orig_schema.enum, field_name, summary))
        if diff_type == DiffType.REQUEST_SCHEMA_MODIFY_READONLY or diff_type == DiffType.RESPONSE_SCHEMA_MODIFY_READONLY:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_schema.read_only, orig_schema.read_only, field_name, summary))
        if diff_type == DiffType.REQUEST_SCHEMA_FIELD_ADD or diff_type == DiffType.RESPONSE_SCHEMA_FIELD_ADD:
            self.diff_list.append(DiffProperty(path, method, diff_type, field_name, None, field_name, summary))
        if diff_type == DiffType.REQUEST_SCHEMA_FIELD_DELETE or diff_type == DiffType.RESPONSE_SCHEMA_FIELD_DELETE:
            self.diff_list.append(DiffProperty(path, method, diff_type, None, field_name, field_name, summary))
        if diff_type == DiffType.REQUEST_SCHEMA_MODIFY_DESC or diff_type == DiffType.RESPONSE_SCHEMA_MODIFY_DESC:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_schema.description, orig_schema.description, field_name, summary))
        if diff_type == DiffType.REQUEST_SCHEMA_MODIFY_REQUIRED or diff_type == DiffType.RESPONSE_SCHEMA_MODIFY_REQUIRED:
            self.diff_list.append(DiffProperty(path, method, diff_type, self.generate_schema_required(new_schema.required, field_name), self.generate_schema_required(orig_schema.required, field_name), field_name, summary))
        if diff_type == DiffType.REQUEST_SCHEMA_MODIFY_ITEMS_TYPE or diff_type == DiffType.RESPONSE_SCHEMA_MODIFY_ITEMS_TYPE:
            self.diff_list.append(DiffProperty(path, method, diff_type, TypeConvertor.convertToActualDataType(new_schema.type, new_schema.format), TypeConvertor.convertToActualDataType(orig_schema.type, orig_schema.format), None, summary))
        if diff_type == DiffType.REQUEST_SCHEMA_MODIFY_EXAMPLE or diff_type == DiffType.RESPONSE_SCHEMA_MODIFY_EXAMPLE:
            self.diff_list.append(DiffProperty(path, method, diff_type, new_schema.example, orig_schema.example, field_name, summary))

    def generate_schema_required(self, required_list, name):
        if required_list is None:
            return False
        return name in required_list

    def diff_responses(self, path, method, summary, new_responses, orig_responses):
        for http_code in new_responses:
            if http_code in orig_responses:
                self.diff_response(path, method, summary, new_responses.get(http_code), orig_responses.get(http_code), http_code)
            else:
                self.build_response_diff(path, method, summary, DiffType.RESPONSE_HTTP_STATUS_ADD, new_responses.get(http_code), None, None, http_code)
        for http_code in orig_responses:
            if http_code not in new_responses:
                self.build_response_diff(path, method, summary, DiffType.RESPONSE_HTTP_STATUS_DELETE, None, orig_responses.get(http_code), None, http_code)

    def build_response_diff(self, path, method, summary, diff_type, new_response, orig_response, field_name, http_code):
        if diff_type == DiffType.RESPONSE_HTTP_STATUS_ADD:
            self.diff_list.append(DiffProperty(path, method, diff_type, http_code, None, None, summary, http_code))
        if diff_type == DiffType.RESPONSE_HTTP_STATUS_DELETE:
            self.diff_list.append(DiffProperty(path, method, diff_type, None, http_code, None, summary, http_code))

    def diff_response(self, path, method, summary, new_response, orig_response, http_code):
        if new_response.description != orig_response.description:
            self.build_response_diff(path, method, summary, DiffType.RESPONSE_PARAMETER_MODIFY_DESC, new_response, orig_response, None, http_code)
        if new_response.schema is not None:
            if new_response.schema.ref is not None:
                self.generate_schema(path, method, summary, new_response.schema.ref, orig_response.schema.ref, PropertyType.RESPONSE)
            else:
                if new_response.schema.type == ShowDataType.ARRAY:
                    self.diff_schema_list(path, method, summary, new_response.schema, orig_response.schema, PropertyType.RESPONSE)
                else:
                    # 单纯的response，不带任何名称，接口直接返回基本类型
                    self.diff_schema_base(path, method, summary, new_response.schema, orig_response.schema, PropertyType.RESPONSE)

    def diff_schema_base(self, path, method, summary, new_schema, orig_schema, property_type):
        suffix = None
        if new_schema.type != orig_schema.type or new_schema.format != orig_schema.format:
            suffix = 'schema_modify_type'
        if suffix:
            self.build_schema_diff(path, method, summary, DiffType.get_diff_type(property_type, suffix), new_schema, orig_schema, None)

    """
    "responses": {
                    "200": {
                        "description": "OK",
                        解析这个schema
                        "schema": {
                            "type": "array",
                            "items": {
                                "type": "integer",
                                "format": "int32"
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized"
                    },
                    "403": {
                        "description": "Forbidden"
                    },
                    "404": {
                        "description": "Not Found"
                    }
                }
    """
    def diff_schema_list(self, path, method, summary, new_schema, orig_schema, property_type):
        new_items = new_schema.items
        orig_items = orig_schema.items
        suffix = None
        if new_items.type != orig_items.type or new_items.format != orig_items.format:
            suffix = 'schema_modify_items_type'
        if suffix:
            self.build_schema_diff(path, method, summary, DiffType.get_diff_type(property_type, suffix), new_items, orig_items, None)