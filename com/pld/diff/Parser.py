#-*- coding: UTF-8 -*-

from com.pld.model.Api import Api
from com.pld.model.Request import Request
from com.pld.model.Property import Property
from com.pld.model.Response import Response
from com.pld.model.Method import Method


class Parser(object):

    def __init__(self, json):
        if json is None:
            raise Exception('the response of input url is empty')
        if 'paths' not in json:
            raise Exception('cannot parse result, please check your input url')
        self.paths = json['paths']
        self.definitions = json['definitions']

    def parse(self):

        if len(self.paths) <= 0:
            return None
        api_dict = {}
        for path in self.paths:
            # if path == '/app-api/chip/overseas/getChipFile':
                method_dict = {}
                path_dict = self.paths[path]
                if 'post' in path_dict:
                    post = path_dict['post']
                    method_dict['post'] = self.parse_method(post, 'post')
                if 'get' in path_dict:
                    get = path_dict['get']
                    method_dict['get'] = self.parse_method(get, 'get')
                if 'delete' in path_dict:
                    delete = path_dict['delete']
                    method_dict['delete'] = self.parse_method(delete, 'delete')
                if 'put' in path_dict:
                    put = path_dict['put']
                    method_dict['put'] = self.parse_method(put, 'put')
                if 'head' in path_dict:
                    head = path_dict['head']
                    method_dict['head'] = self.parse_method(head, 'head')
                api_dict[path] = Api(path, method_dict)
        return api_dict

    def parse_method(self, json, method):
        tags = None
        summary = None
        consumes = None
        produces = None
        parameters = None
        request = None
        responses = None
        response = None
        if 'tags' in json:
            tags = json['tags']
        if 'summary' in json:
            summary = json['summary']
        if 'consumes' in json:
            consumes = json['consumes']
        if 'produces' in json:
            produces = json['produces']
        if 'parameters' in json:
            parameters = json['parameters']
            request = self.parse_request(parameters)
        if 'responses' in json:
            responses = json['responses']
            response = self.parse_response(responses)
        return Method(method, summary, request, response, tags, consumes, produces)

    def parse_request(self, parameters):
        request_list = set()
        for parameter in parameters:
            name = parameter['name']
            required = parameter['required']
            description = parameter.get('description')
            if 'schema' in parameter:
                schema = parameter['schema']
                if '$ref' in schema:
                    # 解析实体名称
                    request_name = self.generate_ref(schema.get('$ref'))
                    # 解析参数
                    params = self.parse_params(request_name)
                    request_list.add(Request(name, required, params['type'], description, params['params']))
                elif 'items' in schema:
                    # list类别的基本类型
                    param_type = schema['type']
                    items = schema['items']
                    request_list.add(Request(name, required, param_type, description, items))
                else:
                    request_list.add(Request(name, required, schema['type'], description, None))
            else:
                # object类别的基本类型
                param_type = parameter['type']
                if param_type == 'integer' or param_type == 'string' or param_type == 'number' or param_type == 'boolean':
                    request_list.add(Request(name, required, param_type, description, None))
        return request_list

    # #/definitions/BaseAuthRequest
    def generate_ref(self, ref_name):
        if ref_name is None:
            return
        begin_index = ref_name.rfind('/', 0, len(ref_name));
        if begin_index == -1:
            return
        return ref_name[begin_index + 1:]

    def parse_params(self, name):
        params = {}
        if name in self.definitions:
            definition = self.definitions[name]
            # BackendGetParentNodeInfoReq: {type: "object",…}，获取此处的实体type
            param_type = definition['type']
            params['type'] = param_type
            if param_type == 'object':
                params['params'] = self.parse_object(definition, name)
            elif param_type == 'array':
                params['params'] = self.parse_array(definition)
        return params

    def parse_object(self, json, parent_ref):
        required_list = set()
        params = set()
        # 获取必填requiredList
        if 'required' in json:
            required_list = json['required']
        # 获取所有参数
        if 'properties' in json:
            properties = json['properties']
            for property_name in properties:
                # 获取property的json
                property_item = properties[property_name]
                required = False
                # 判断参数是否必填
                if property_name in required_list:
                    required = True
                # 该参数是否为引用类型，如果是，需要递归追溯
                if '$ref' in property_item:
                    ref = self.generate_ref(property_item.get('$ref'))
                    if parent_ref == ref:
                        # 有可能存在A引用了B，B自身又引用了B，此时需要终止，否则陷入死循环
                        params.add(Property(property_name, property_item.get('type'), property_item.get('description'), required, None, parent_ref))
                    else:
                        ref_params = self.parse_params(ref)
                        params.add(Property(property_name, ref_params['type'], property_item.get('description'), required, ref_params['params'], None))
                # 该参数是否为列表类型
                elif 'items' in property_item:
                    items = property_item.get('items')
                    if '$ref' in items:
                        # 引用类型
                        ref = self.generate_ref(items.get('$ref'))
                        if parent_ref == ref:
                            # 有可能存在A引用了B，B自身又引用了B，此时需要终止，否则陷入死循环
                            params.add(Property(property_name, property_item.get('type'), property_item.get('description'), required, None, parent_ref))
                        else:
                            ref_params = self.parse_params(ref)
                            params.add(Property(property_name, ref_params['type'], property_item.get('description'), required, ref_params['params'], None))
                    else:
                        # 普通类型
                        params.add(Property(property_name, property_item.get('type'), property_item.get('description'), required, None, None))
                else:
                    property_type = property_item.get('type')
                    property_description = property_item.get('description')
                    if property_type == 'object':
                        params.add(Property(property_name, property_type, property_description, required, None, None))
                    elif property_type == 'array':
                        items = self.parse_array(property_item.get('items'))
                        params.add(Property(property_name, property_type, property_description, required, items, None))
                    elif property_type == 'string' or property_type == 'integer' or property_type == 'boolean' or property_type == 'number':
                        params.add(Property(property_name, property_type, property_description, required, None, None))
        return params

    def parse_response(self, response):
        # 只处理200 响应码的响应参数
        success_response = response.get('200')
        if 'schema' in success_response:
            schema = success_response.get('schema')
            if '$ref' in schema:
                # 引用类型
                return self.parse_response_ref(schema.get('$ref'))
            elif 'type' in schema:
                # 普通类型
                return Response(schema.get('type'), None)

    def parse_array(self, items):
        params = set()
        if '$ref' in items:
            ref_name = self.generate_ref(items.get('$ref'))
            params = self.parse_params(ref_name)
        for item in items:
            type = item.get('type')
            if type == 'object':
                params.add(self.parse_object(item, None))
            elif type == 'array':
                params.add(self.parse_array(item))
        return params

    def parse_response_ref(self, ref):
        if ref is None:
            return None
        ref_name = self.generate_ref(ref)
        params = self.parse_params(ref_name)
        return Response(params['type'], params['params'])
