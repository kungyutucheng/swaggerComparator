# -*- coding: UTF-8 -*-
import sys
from ListUtil import ListUtil

reload(sys)
sys.setdefaultencoding('utf8')


class HtmlGenerator(object):

    @staticmethod
    def generate_diff_html(new_url, orig_url, diff_property_list):

        html = """
        <html>
        <head>
        <title>swagger对比结果</title>
        <style>
        table, td, th
        {
        border:1px solid black;
        border-radius: 2px;
        }
        td
        {
        padding:10px;
        }
        table tr th{
        background: #ffd;
        }
        table tr:nth-child(odd){
        background: #F5F5F5;
        }	
        table tr:nth-child(even){
        background: #efe;
        }	
        </style>
        </head>
         <body>
        <p>当前版本：%s</p><br/>
        <p>对比版本：%s</p><br/>
        <table><tr>
        <th>序号</th>
        <th>接口url</th>
        <th>method</th>
        <th>改动类型</th>
        <th>字段名称</th>
        <th>响应码</th>
        <th>旧值</th>
        <th>新值</th>
        <th>备注</th>
        </tr>
        """ % (new_url, orig_url)

        index = 1
        for diff_property in diff_property_list:
            # 处理None
            if diff_property.path is None:
                diff_property.path = ''
            if diff_property.method is None:
                diff_property.method = ''
            if diff_property.diff_type is None:
                diff_property.diff_type = ''
            if diff_property.field_name is None:
                diff_property.field_name = ''
            if diff_property.http_code is None:
                diff_property.http_code = ''
            if diff_property.orig_value is None:
                diff_property.orig_value = ''
            if diff_property.new_value is None:
                diff_property.new_value = ''
            if diff_property.remark is None:
                diff_property.remark = ''

            # 处理list
            if type(diff_property.orig_value) == list:
                diff_property.orig_value = ListUtil.joinList(diff_property.orig_value, ',')
            if type(diff_property.new_value) == list:
                diff_property.new_value = ListUtil.joinList(diff_property.new_value, ',')

            if '删除' in diff_property.diff_type:
                html += """
                <tr>
                <td><s>%s<s></td>
                <td><s>%s<s></td>
                <td><s>%s<s></td>
                <td><s>%s<s></td>
                <td><s>%s<s></td>
                <td><s>%s<s></td>
                <td><s>%s<s></td>
                <td><s>%s<s></td>
                <td><s>%s<s></td>
                </tr>
                """ % (index, diff_property.path, diff_property.method, diff_property.diff_type, diff_property.field_name, diff_property.http_code, diff_property.orig_value, diff_property.new_value, diff_property.remark)
            else:
                html += """
                <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                </tr>
                """ % (index, diff_property.path, diff_property.method, diff_property.diff_type, diff_property.field_name, diff_property.http_code, diff_property.orig_value, diff_property.new_value, diff_property.remark)

            index += 1
        html += """
        </table>
        </body>
        </html>
        """

        return html


if __name__ == '__main__':
    print(reduce(lambda v1,v2 : v2 + v1, map(lambda v: v + ',',['1','2','2'])))


