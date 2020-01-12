# -*- coding: UTF-8 -*-
import sys
import requests
import json
from Parser import Parser
sys.path.append('..')
from model.v3.OpenApi import OpenApi
from model.v3.Schema import Schema
from model.v3.Server import Server
from model.v3.ServerValue import ServerValue
from model.v3.Response import Response
from model.v3.RequestBody import RequestBody
from model.v3.Parameter import Parameter
from model.v3.Operation import Operation
from model.v3.PathItem import PathItem
from model.v3.Component import Component
from model.v3.Discriminator import Discriminator
from model.v3.Encoding import Encoding
from model.v3.Example import Example
from model.v3.Link import Link
from model.v3.MediaType import MediaType
from model.v3.SecuritySchema import SecuritySchema
from model.v3.OAuthFlow import OAuthFlow


reload(sys)
sys.setdefaultencoding('utf8')


class OpenApiParser(Parser):

    def __init__(self, json):
        self.parser = Parser()
        self.json = json

    def parse(self):
        openapi = OpenApi()
        openapi.open_api = self.json.get('openApi')
        openapi.info = self.parser.parse_info(self.json.get('info'))
        openapi.servers = self.parse_servers(self.json.get('servers'))
        openapi.paths = self.parse_paths(self.json.get('paths'))
        openapi.components = self.parse_components(self.json.get('components'))
        return openapi

    def parse_servers(self, servers_json):
        servers = []
        if servers_json is None:
            return servers
        for server_json in servers_json:
            servers.append(self.parse_server(server_json))
        return servers

    def parse_server(self, server_json):
        if server_json is None:
            return None
        server = Server()
        server.description = server_json.get('description')
        server.url = server_json.get('url')
        server.variables = self.parse_server_variables(server_json.get('variables'))
        return server

    def parse_server_variables(self, server_variables_json):
        variables = {}
        if server_variables_json is None:
            return variables
        for name in server_variables_json:
            variables[name] = self.parse_server_value(server_variables_json.get(name))
        return variables

    def parse_server_value(self, server_value_json):
        if server_value_json is None:
            return None
        server_value = ServerValue()
        server_value.description = server_value_json.get('description')
        server_value.default = server_value_json.get('default')
        server_value.enum = server_value_json.get('enum')
        return server_value

    def parse_paths(self, paths_json):
        paths = {}
        if paths_json is None:
            return paths
        for url in paths_json:
            path_item = PathItem()
            operate_map = {}
            path_item_json = paths_json.get(url)
            for method in path_item_json:
                operate_map[method] = self.parse_operation(path_item_json.get(method))
            path_item.operation_map = operate_map
            path_item.ref = path_item_json.get('ref')
            path_item.description = path_item_json.get('description')
            path_item.servers = self.parse_servers(path_item_json.get('servers'))
            path_item.parameters = self.parse_parameters(path_item_json.get('parameters'))
            paths[url] = path_item
        return paths

    def parse_operation(self, operation_json):
        if operation_json is None:
            return None
        operation = Operation()
        operation.tags = operation_json.get('tags')
        operation.summary = operation_json.get('summary')
        operation.description = operation_json.get('description')
        operation.external_docs = self.parse_external_docs(operation_json.get('externalDocs'))
        operation.operation_id = operation_json.get('operationId')
        operation.parameters = self.parse_parameters(operation_json.get('parameters'))
        operation.request_body = self.parse_request_body(operation_json.get('requestBody'))
        operation.responses = self.parse_responses(operation_json.get('responses'))
        operation.callbacks = operation_json.get('callbacks')
        operation.deprecated = operation_json.get('deprecated')
        operation.security = self.parse_security(operation_json.get('security'))
        operation.servers = self.parse_servers(operation_json.get('servers'))
        return operation

    def parse_parameters(self, parameters_json):
        parameters = []
        if parameters_json is None:
            return parameters
        for parameter_json in parameters_json:
            parameters.append(self.parse_parameter(parameter_json))
        return parameters

    def parse_schema(self, schema_json):
        if schema_json is None:
            return None
        if '$ref' in schema_json:
            return schema_json
        else:
            schema = Schema()
            self.parse_base_parameter(schema, schema_json)
            self.parse_base_base_parameter(schema, schema_json)

            schema.discriminator = self.parse_discriminator(schema_json.get('discriminator'))
            schema.write_only = schema_json.get('write_only')
            schema.deprecated = schema_json.get('deprecated')
            schema.example = schema_json.get('example')
            schema.xml = self.parser.parse_xml(schema_json.get('xml'))
            schema.external_docs = self.parse_external_docs(schema_json.get('externalDocs'))
            schema.nullable = schema_json.get('nullable')
            schema.title = schema_json.get('title')

            schema.all_of = self.parse_schema_properties(schema_json.get('allOf'))
            schema.properties = self.parse_schema_properties(schema_json.get('properties'))
            schema.any_of = self.parse_schema_properties(schema_json.get('anyOf'))
            schema.one_of = self.parse_schema_properties(schema_json.get('oneOf'))
            schema.additional_properties = self.parse_schema(schema_json.get('additionalProperties'))
            schema.not_ = self.parse_schema_properties(schema_json.get('not'))
            schema.items = self.parse_schema(schema_json.get('items'))
            return schema

    def parse_schema_properties(self, properties_json):
        properties = {}
        if properties_json is None:
            return properties
        if '$ref' in properties_json:
            properties = properties_json
        else:
            for name in properties_json:
                properties[name] = self.parse_schema(properties_json.get(name))
        return properties

    def parse_examples(self, examples_json):
        examples = {}
        if examples_json is None:
            return examples
        for name in examples_json:
            example = Example()
            example_json = examples_json.get(name)
            example.summary = example_json.get('summary')
            example.description = example_json.get('description')
            example.external_value = example_json.get('externalValue')
            example.value = example_json.get('value')
            examples[name] = example_json
        return examples

    def parse_contents(self, contents_json):
        contents = {}
        if contents_json is None:
            return contents
        for name in contents_json:
            content_json = contents_json.get(name)
            contents[name] = self.parse_content(content_json)
        return contents

    def parse_content(self, content_json):
        if content_json is None:
            return None
        media_type = MediaType()
        schema_json = content_json.get('schema')
        if '$ref' in schema_json:
            media_type.schema = schema_json
        else:
            media_type.schema = self.parse_schema(schema_json)
        media_type.example = content_json.get('example')
        media_type.examples = self.parse_examples(content_json.get('examples'))
        media_type.encoding = self.parse_encodings(content_json.get('encoding'))
        return media_type

    def parse_encodings(self, encodings_json):
        encodings = {}
        if encodings_json is None:
            return encodings
        for name in encodings_json:
            encoding_json = encodings_json.get(name)
            encoding = Encoding()
            encoding.content_type =  encoding_json.get('contentType')
            encoding.headers = self.parse_headers(encoding_json.get('headers'))
            encoding.style = encoding_json.get('style')
            encoding.explode = encoding_json.get('explode')
            encoding.allow_reserved = encoding_json.get('allow_reserved')
            encodings[name] = encoding
        return encodings

    def parse_headers(self, headers_json):
        headers = {}
        if headers_json is None:
            return headers
        for name in headers_json:
            header_json = headers_json.get(name)
            if '$ref' in header_json:
                headers[name] = header_json
            else:
                headers[name] = self.parse_parameter(header_json)
        return headers

    def parse_parameter(self, parameter_json):
        if '$ref' in parameter_json:
            return parameter_json
        else:
            parameter = Parameter()
            self.parser.parse_base_parameter(parameter, parameter_json)
            parameter.deprecated = parameter_json.get("deprecated")
            parameter.allow_empty_value = parameter_json.get('allowEmptyValue')
            parameter.style = parameter_json.get('style')
            parameter.explode = parameter_json.get('explode')
            parameter.allow_reserved = parameter_json.get('allowReserved')
            schema_json = parameter_json.get('schema')
            if '$ref' in schema_json:
                parameter.schema = schema_json
            else:
                parameter.schema = self.parse_schema(schema_json)
            parameter.example = parameter_json.get('example')
            parameter.examples = self.parse_examples(parameter_json.get('examples'))
            parameter.content = self.parse_contents(parameter_json.get('content'))
            return parameter

    def parse_discriminator(self, discriminator_json):
        if discriminator_json is None:
            return None
        discriminator = Discriminator()
        discriminator.property_name = discriminator_json.get('propertyName')
        discriminator.mapping = discriminator_json.get('mapping')
        return discriminator

    def parse_request_body(self, request_body_json):
        if request_body_json is None:
            return None
        if '$ref' in request_body_json:
            return request_body_json
        else:
            request_body = RequestBody()
            request_body.description = request_body_json.get('description')
            request_body.content = self.parse_contents(request_body_json.get('content'))
            request_body.required = request_body_json.get('required')
            return request_body

    def parse_responses(self, responses_json):
        responses = {}
        if responses_json is None:
            return responses
        for code in responses_json:
            responses[code] = self.parse_response(responses_json.get(code))
        return responses

    def parse_response(self, response_json):
        if response_json is None:
            return None
        response = Response()
        response.description = response_json.get('description')
        response.headers = self.parse_headers(response_json.get('headers'))
        response.links = self.parse_links(response_json.get('links'))
        response.content = self.parse_contents(response_json.get('content'))
        return response

    def parse_links(self, links_json):
        links = {}
        if links_json is None:
            return links
        for name in links_json:
            links[name] = self.parse_link(links_json.get(name))
        return links

    def parse_link(self, link_json):
        if link_json is None:
            return None
        link = Link()
        link.description = link_json.get('description')
        link.request_body = link_json.get('requestBody')
        link.parameters = link_json.get('parameters')
        link.operation_id = link_json.get('operationId')
        link.server = self.parse_servers(link_json.get('servers'))
        link.operation_ref = link_json.get('operationRef')
        return link

    def parse_security(self, security_json):
        security = {}
        if security_json is None:
            return security
        for name in security_json:
            security[name] = security_json.get(name)
        return security

    def parse_components(self, components_json):
        component = Component()
        component.schemas = self.parse_schemas(components_json.get('schemas'))
        component.responses = self.parse_responses(components_json.get('responses'))
        component.parameters = self.parse_parameters_map(components_json.get('parameters'))
        component.examples = self.parse_examples(components_json.get('examples'))
        component.request_bodies = self.parse_request_bodies(components_json.get('requestBodies'))
        component.headers = self.parse_headers(components_json.get('headers'))
        component.security_schemes = self.parse_security_schemas(components_json.get('securitySchemas'))
        component.links = self.parse_links(components_json.get('links'))
        component.callbacks = components_json.get('callbacks')
        return component

    def parse_schemas(self, schemas_json):
        schemas = {}
        if schemas_json is None:
            return schemas
        for name in schemas_json:
            schemas[name] = self.parse_schema(schemas_json.get(name))
        return schemas

    def parse_request_bodies(self, request_bodies_json):
        request_bodies = {}
        if request_bodies_json is None:
            return request_bodies
        for name in request_bodies:
            request_bodies[name] = self.parse_request_body(request_bodies_json.get(name))
        return request_bodies

    def parse_security_schemas(self, security_schemas_json):
        security_schemas = {}
        if security_schemas_json is None:
            return security_schemas
        for name in security_schemas_json:
            security_schemas[name] = self.parse_secuirty_schema(security_schemas_json.get(name))
        return security_schemas

    def parse_secuirty_schema(self, security_schema_json):
        if security_schema_json is None:
            return None
        if '$ref' in security_schema_json:
            return security_schema_json
        else:
            security_schema = SecuritySchema()
            security_schema.name = security_schema_json.get('name')
            security_schema.description = security_schema_json.get('description')
            security_schema.schema = security_schema_json.get('schema')
            security_schema.type = security_schema_json.get('type')
            security_schema.in_ = security_schema_json.get('in')
            security_schema.bearer_format = security_schema_json.get('bearerFormat')
            security_schema.flows = self.parse_flows(security_schema_json.get('flows'))
            security_schema.open_id_connect_url = security_schema_json.get('openIdConnectUrl')
            return security_schema

    def parse_flows(self, flows_json):
        flows = {}
        if flows_json is None:
            return flows
        for name in flows_json:
            flows[name] = self.parse_flow(flows_json.get(name))
        return flows

    def parse_flow(self, flow_json):
        if flow_json is None:
            return None
        flow = OAuthFlow()
        flow.authorization_url = flow_json.get('authorizationUrl')
        flow.token_url = flow_json.get('tokenUrl')
        flow.refresh_url = flow_json.get('refreshUrl')
        flow.scopes = flow_json.get('scopes')
        return flow

    def parse_parameters_map(self, parameters_json):
        parameters = {}
        if parameters_json is None:
            return parameters
        for name in parameters_json:
            parameters[name] = self.parse_parameter(parameters_json.get(name))
        return parameters


if __name__ == '__main__':
    new_response = requests.request("get", 'https://generator3.swagger.io/openapi.json')
    new_json = json.loads(new_response.content)
    parse = OpenApiParser(new_json)
    parse.parse()