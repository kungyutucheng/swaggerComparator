# -*- coding: UTF-8 -*-
import sys

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
        <th>接口url</th>
        <th>method</th>
        <th>改动类型</th>
        <th>旧值</th>
        <th>新值</th>
        <th>字段名称</th>
        </tr>
        """ % (new_url, orig_url)

        for diff_property in diff_property_list:
            if diff_property.diff_type.contains("删除"):
                html += """
                <tr>
                <td><s>%s<s></td>
                <td><s>%s<s></td>
                <td><s>%s<s></td>
                <td><s>%s<s></td>
                <td><s>%s<s></td>
                <td><s>%s<s></td>
                </tr>
                """ % (diff_property.path, diff_property.method, diff_property.diff_type, diff_property.orig_value, diff_property.new_value, diff_property.field_name)
            else:
                html += """
                <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                </tr>
                """ % (diff_property.path, diff_property.method, diff_property.diff_type, diff_property.orig_value, diff_property.new_value, diff_property.field_name)

        html += """
        </table>
        </body>
        </html>
        """

        return html




