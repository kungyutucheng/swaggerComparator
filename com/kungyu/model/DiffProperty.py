# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class DiffProperty(object):
    def __init__(self, path, method, diff_type, new_value, orig_value, field_name=None, remark=None, http_code=None):
        self.path = path
        self.method = method
        self.diff_type = diff_type
        self.orig_value = orig_value
        self.new_value = new_value
        self.field_name = field_name
        self.remark = remark
        self.http_code = http_code

    def to_tr_html(self):
        empty_td = '<td></td>'
        html = '<tr>'
        html += '<td>' + self.path + '</td>'
        html += '<td>' + self.method + '</td>'
        html += '<td>' + self.diff_type + '</td>'
        if self.orig_value:
            html += '<td>' + self.orig_value + '</td>'
        else:
            html += empty_td
        if self.new_value:
            html += '<td>' + self.new_value + '</td>'
        else:
            html += empty_td
        if self.field_name:
            html += '<td>' + self.field_name + '</td>'
        else:
            html += empty_td
        html += '</tr>'
        return html