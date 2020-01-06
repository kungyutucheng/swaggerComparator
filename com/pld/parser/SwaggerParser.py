# -*- coding: UTF-8 -*-
import sys
import requests
import json
from Parser import Parser
from com.pld.model.v2.Swagger import Swagger
from com.pld.model.v2.Schema import Schema
from com.pld.model.v2.Response import Response
from com.pld.model.v2.Parameter import Parameter
from com.pld.model.v2.Operation import Operation
from com.pld.model.v2.PathItem import PathItem
from com.pld.enums.InType import InType
from com.pld.model.v2.Item import Item
from com.pld.model.v2.SecuritySchema import SecuritySchema

reload(sys)
sys.setdefaultencoding('utf8')


class SwaggerParser(Parser):

    def __init__(self, json):
        self.parser = Parser()
        self.json = json

    def parse(self):
        swagger = Swagger()
        swagger.swagger = self.json.get('swagger')
        swagger.info = self.parser.parse_info(self.json.get('info'))
        swagger.host = self.json.get('host')
        swagger.base_path = self.json.get('basePath')
        swagger.schemes = self.json.get('schemes')
        swagger.consumes = self.json.get('consumes')
        swagger.produces = self.json.get('produces')
        swagger.paths = self.parse_path(self.json.get('paths'))
        swagger.definitions = self.parse_definitions(self.json.get('definitions'))
        swagger.parameters = self.parse_parameters(self.json.get('parameters'))
        swagger.responses = self.parse_responses(self.json.get('responses'))
        swagger.security_definitions = self.parse_security_definitions(self.json.get('securityDefinitions'))
        swagger.security = self.parse_security(self.json.get('security'))
        swagger.tags = self.parser.parse_tags(self.json.get('tags'))
        swagger.external_docs = self.parser.parse_external_docs(self.json.get('externalDocs'))
        return swagger

    def parse_path(self, paths_dict):
        paths = {}
        if json is None:
            return paths
        for url in paths_dict:
            path_item = PathItem()
            operation_map = {}
            parameters = []
            path_item_dict = paths_dict.get(url)
            for method in path_item_dict:
                if method is 'get' or 'put' or 'post' or 'delete' or 'options' or 'head' or 'patch':
                    operation_map[method] = self.parse_operation(path_item_dict.get(method))
                elif method is '$ref':
                    self.parser.parse_path_item(path_item, path_item_dict.get(method))
                else:
                    parameters.append(self.parse_parameters(path_item_dict.get('parameters')))
            path_item.operation_map = operation_map
            path_item.parameters = parameters
            paths[url] = path_item
        return paths

    def parse_parameters(self, json):
        parameters = []
        if json is None:
            return parameters
        for parameter_json in json:
            parameter = Parameter()
            self.parse_parameter(parameter, parameter_json)
            parameters.append(parameter)
        return parameters

    def parse_parameter(self, parameter, parameter_json):
        self.parser.parse_base_parameter(parameter, parameter_json)
        if parameter.in_ == InType.BODY:
            parameter.schema = self.parse_schema(parameter_json.get('schema'))
        else:
            self.parser.parse_base_base_parameter(parameter, parameter_json)
            self.parse_base_items(parameter, parameter_json.get('items'))

    def parse_responses(self, responses_json):
        responses = {}
        if responses_json is None:
            return responses
        for code in responses_json:
            response = Response()
            response_json = responses_json.get(code)
            self.parser.parse_base_response(response, response_json)
            response.headers = self.parse_headers(response_json.get('headers'))
            response.schema = self.parse_schema(response_json.get('schema'))
            response.examples = self.parse_examples(response_json.get('examples'))
            responses[code] = response
        return responses

    def parse_security_definitions(self, security_definitions_json):
        security_definitions = {}
        if security_definitions_json is None:
            return security_definitions
        for name in security_definitions_json:
            security_definition = security_definitions_json.get(name)
            security_schema = SecuritySchema()
            security_schema.type = security_definition.get('type')
            security_schema.description = security_definition.get('description')
            security_schema.name = security_definition.get('name')
            security_schema.in_ = security_definition.get('in')
            security_schema.flow = security_definition.get('flow')
            security_schema.authorization_url = security_definition.get('authorizationUrl')
            security_schema.token_url = security_definition.get('tokenUrl')
            self.parser.parse_base_scope(security_schema, security_definition.get('scopes'))
            security_definitions[name] = security_schema
        return security_definitions

    def parse_security(self, security_json):
        security = {}
        if security_json is None:
            return security
        for name in security_json:
            security[name] = security_json.get(name)
        return security

    def parse_definitions(self, definitions_json):
        definitions = {}
        if definitions_json is None:
            return definitions
        for definition in definitions_json:
            definitions[definition] = self.parse_schema(definitions_json.get(definition))
        return definitions

    def parse_operation(self, json):
        if json is None:
            return None
        operation = Operation()
        self.parse_base_operation(operation, json)
        operation.parameters = self.parse_parameters(json.get('parameters'))
        operation.responses = self.parse_responses(json.get('responses'))
        operation.consumes = self.parser.parse_consumes(json.get('consumes'))
        operation.produces = self.parser.parse_produces(json.get('produces'))
        return operation

    def parse_schema(self, schema_json):
        if schema_json is None:
            return None
        schema = Schema()
        self.parser.parse_base_schema(schema, schema_json)
        schema.ref = schema_json.get('$ref')
        schema.description = schema_json.get('description')
        schema.discriminator = schema_json.get('discriminator')

        # parse all of
        schema.all_of = self.parse_schema_properties(schema_json.get('allOf'))
        # parse properties
        schema.properties = self.parse_schema_properties(schema_json.get('properties'))
        schema.additional_properties = self.parse_schema_properties(schema_json.get('additional_properties'))
        schema.items = self.parse_schema(schema_json.get('items'))
        return schema

    """
    "AccountGetNeedGuideStatusResp": {
            "type": "object",
            "required": [
                "needGuideStatus"
            ],
            "properties": {
                "needGuideStatus": {
                    "type": "string",
                    "description": "客户是否需要引导，1:需要，2:不需要"
                }
            }
        }
    """
    def parse_schema_properties(self, properties_json):
        properties = {}
        if properties_json is None:
            return properties
        for name in properties_json:
            properties[name] = self.parse_schema(properties_json.get(name))
        return properties

    def parse_headers(self, headers_json):
        headers = {}
        if headers_json is None:
            return headers
        for header_name in headers_json:
            # the structure of header here is the same as parameter, so we can parse it in parameter way
            header = Parameter()
            self.parse_parameter(header, headers_json.get(header_name))
            headers[header_name] = header
        return headers

    def parse_base_items(self, parameter, items_json):
        if items_json is None:
            return None
        item = Item()
        self.parser.parse_base_base_parameter(item, items_json)
        parameter.items = item

    def parse_examples(self, examples_json):
        examples = {}
        if examples_json is None:
            return examples
        for mime_type in examples_json:
            examples[mime_type] = examples_json.get(mime_type)
        return examples


if __name__ == '__main__':
    new_response = requests.request("get", 'http://14.29.176.173:8089/fengyingcun/v2/api-docs')
    new_json = json.loads(new_response.content)
    parse = SwaggerParser(new_json)
    parse.parse()

