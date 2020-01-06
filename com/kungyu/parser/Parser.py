# -*- coding: UTF-8 -*-
import sys

from com.kungyu.model.common.Contact import Contact
from com.kungyu.model.common.Info import Info
from com.kungyu.model.common.ExternalDocumentation import ExternalDocumentation
from com.kungyu.model.common.Tag import Tag
from com.kungyu.model.common.License import License
from com.kungyu.model.base.Schema import Schema
from com.kungyu.model.common.Xml import Xml
from com.kungyu.model.base.BaseParameter import BaseParameter

reload(sys)
sys.setdefaultencoding('utf8')



class Parser(object):

        # if json is None:
        #     raise Exception('the response of input url is empty')
        # if 'swagger' in json:
        #     self.parser = SwaggerParser()
        # elif 'openapi' in json:
        #     self.parser = OpenApiParser()
        # else:
        #     raise Exception('cannot parse result, please check your input url')

    def parse(self):
        pass

    def parse_info(self, info_json):
        if info_json is None:
            return None
        info = Info()
        info.title = info_json.get('title')
        info.description = info_json.get('description')
        info.terms_of_service = info_json.get('termsOfService')
        info.contact = self.parse_contact(info_json.get('contact'))
        info.license = self.parse_license(info_json.get('license'))
        info.version = info_json.get('version')
        return info

    def parse_contact(self, contact_json):
        if contact_json is None:
            return None
        contact = Contact()
        contact.name = contact_json.get('name')
        contact.url = contact_json.get('url')
        contact.email = contact_json.get('email')
        return contact

    def parse_license(self, license_json):
        if license_json is None:
            return None
        license = License()
        license.name = license_json.get('name')
        license.url = license_json.get('url')
        return license_json

    def parse_tags(self, tags_json):
        tags = []
        if tags_json is None:
            return tags
        for tag_json in tags_json:
            tag = Tag()
            tag.name = tag_json.get('name')
            tag.description = tag_json.get('description')
            tag.external_docs = self.parse_external_docs(tag_json.get('externalDocs'))
            tags.append(tag)
        return tags

    def parse_external_docs(self, external_docs_json):
        if external_docs_json is None:
            return None
        external_docs = ExternalDocumentation()
        external_docs.description = external_docs_json.get('description')
        external_docs.url = external_docs_json.get('url')
        return external_docs

    def parse_xml(self, xml_json):
        if xml_json is None:
            return None
        xml = Xml()
        xml.name = xml_json.get('name')
        xml.prefix = xml_json.get('prefix')
        xml.attribute = xml_json.get('attribute')
        xml.namespace = xml_json.get('namespace')
        xml.wrapped = xml_json.get('wrapped')
        return xml

    def parse_path_item(self, path_item, json):
        if json is None:
            return None
        path_item.url = json.get('$ref')
        return path_item

    def parse_base_operation(self, operation, json):
        if json is None:
            return None
        operation.tags = json.get('tags')
        operation.summary = json.get('summary')
        operation.description = json.get('description')
        operation.external_docs = self.parse_external_docs(json.get('externalDocs'))
        operation.operation_id = json.get('operationId')
        operation.deprecated = json.get('deprecated')

    def parse_base_parameter(self, parameter, json):
        if json is None:
            return None
        parameter.name = json.get('name')
        parameter.in_ = json.get('in')
        parameter.description = json.get('description')
        parameter.required = json.get('required')

    def parse_base_base_parameter(self, parameter, json):
        if json is None:
            return None
        parameter.type = json.get('type')
        parameter.format = json.get('format')
        parameter.collection_format = json.get('collectionFormat')
        parameter.default = json.get('default')
        parameter.maximum = json.get('maximum')
        parameter.exclusive_maximum = json.get('exclusiveMaximum')
        parameter.minimum = json.get('minimum')
        parameter.exclusive_minimum = json.get('exclusiveMinimum')
        parameter.max_length = json.get('maxLength')
        parameter.min_length = json.get('minLength')
        parameter.pattern = json.get('pattern')
        parameter.max_items = json.get('maxItems')
        parameter.min_items = json.get('minItems')
        parameter.unique_items = json.get('uniqueItems')
        parameter.enum = json.get('enum')
        parameter.multiple_of = json.get('multipleOf')



    def parse_consumes(self, consumes_json):
        consumes = []
        if consumes_json is None:
            return consumes
        for consume in consumes_json:
            consumes.append(consume)
        return consumes

    def parse_produces(self, produces_json):
        produces = []
        if produces_json is None:
            return produces
        for produce in produces_json:
            produces.append(produce)
        return produces

    def parse_base_schema(self, schema, schema_json):
        if schema_json is None:
            return
        self.parse_base_base_parameter(schema, schema_json)
        schema.title = schema_json.get('title')
        schema.read_only = schema_json.get('readOnly')
        schema.xml = self.parse_xml(schema_json.get('xml'))
        schema.external_docs = self.parse_external_docs(schema_json.get('externalDocs'))
        schema.example = schema_json.get('example')

    def parse_base_response(self, response, response_json):
        if response_json is None:
            return
        response.description = response_json.get('description')

    def parse_base_scope(self, security_schema, scopes_json):
        if scopes_json is None:
            return None
        scopes = {}
        for name in scopes_json:
            scopes[name] = scopes_json.get(name)
        security_schema.scopes = scopes

