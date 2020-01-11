# -*- coding: UTF-8 -*-

from enum import Enum


class DiffType(Enum):
    HOST = '地址修改'

    BASE_PATH = '上下文修改'

    API_METHOD_DELETE = '删除接口method'
    API_METHOD_ADD = '新增接口method'
    API_ADD = '新增接口'
    API_DELETE = '删除接口'
    API_METHOD_MODIFY_SUMMARY = '修改接口名称'
    API_METHOD_MODIFY_TAGS = '修改接口标签'
    API_METHOD_MODIFY_DESCRIPTION = '修改接口描述'
    API_METHOD_MODIFY_CONSUMES = '修改请求content-type'
    API_METHOD_MODIFY_PRODUCES = '修改响应content-type'
    API_METHOD_MODIFY_DEPRECATED = '修改接口弃用值'

    REQUEST_PARAMETER_ADD = '新增入参'
    REQUEST_PARAMETER_DELETE = '删除入参'
    REQUEST_PARAMETER_MODIFY_TYPE = '修改入参类型'
    REQUEST_PARAMETER_MODIFY_DESC = '修改入参定义'
    REQUEST_PARAMETER_MODIFY_REQUIRED = '修改入参必填'
    REQUEST_PARAMETER_MODIFY_REF = '修改入参引用类型'
    REQUEST_SCHEMA_MODIFY_TYPE = '修改入参类型'
    REQUEST_SCHEMA_MODIFY_READONLY = '修改入参只读'
    REQUEST_SCHEMA_MODIFY_ALLOW_VALUES = '修改入参参数可选值'
    REQUEST_SCHEMA_FIELD_ADD = '新增入参'
    REQUEST_SCHEMA_FIELD_DELETE = '删除入参'
    REQUEST_SCHEMA_MODIFY_DESC = '修改入参定义'
    REQUEST_SCHEMA_MODIFY_REQUIRED = '修改入参必填'
    REQUEST_SCHEMA_MODIFY_ITEMS_TYPE = '修改入参列表类型'

    RESPONSE_HTTP_STATUS_ADD = '新增响应状态码'
    RESPONSE_HTTP_STATUS_DELETE = '删除响应状态码'
    RESPONSE_PARAMETER_ADD = '新增出参'
    RESPONSE_PARAMETER_DELETE = '删除出参'
    RESPONSE_PARAMETER_MODIFY_TYPE = '修改出参类型'
    RESPONSE_PARAMETER_MODIFY_DESC = '修改出参定义'
    RESPONSE_PARAMETER_MODIFY_REQUIRED = '修改出参必填'
    RESPONSE_PARAMETER_MODIFY_REF = '修改出参引用类型'
    RESPONSE_SCHEMA_MODIFY_TYPE = '修改出参类型'
    RESPONSE_SCHEMA_MODIFY_READONLY = '修改出参只读'
    RESPONSE_SCHEMA_MODIFY_ALLOW_VALUES = '修改出参参数可选值'
    RESPONSE_SCHEMA_FIELD_ADD = '新增出参'
    RESPONSE_SCHEMA_FIELD_DELETE = '删除出参'
    RESPONSE_SCHEMA_MODIFY_DESC = '修改出参定义'
    RESPONSE_SCHEMA_MODIFY_REQUIRED = '修改出参必填'
    RESPONSE_SCHEMA_MODIFY_ITEMS_TYPE = '修改出参列表类型'

    @staticmethod
    def get_diff_type(prefix, suffix):
        for diff_type in DiffType.__dict__:
            if (prefix + '_' + suffix).upper() == diff_type:
                return DiffType.__getattribute__(DiffType, diff_type)
        return None