# -*- coding: utf-8 -*- 
"""
Author: JerryLaw
Time: 2024/4/18 9:10
Email: 623487850@qq.com
"""
import urllib.parse
import base64


class Encoder:
    @staticmethod
    def __encode_uri_component(component):
        # 使用urllib.parse.quote进行URL编码，并指定safe参数为空字符串，
        # 意味着对除字母数字外的所有字符都进行编码。
        return urllib.parse.quote(component, safe='')

    @staticmethod
    def __unescape(s):
        # JavaScript的escape函数编码的字符映射
        escape_map = {
            '%26': '&', '%2B': '+', '%2F': '/', '%3D': '=', '%3F': '?',
            '%24': '$', '%2C': ',', '%3A': ':', '%3B': ';', '%40': '@',
            '%23': '#', '%25': '%',
            # 添加其他需要解码的字符映射...
        }

        # 首先替换所有的%xx编码
        for key, value in escape_map.items():
            s = s.replace(key, value)

            # 然后处理剩下的%xx编码（这些可能是URL编码的字符）
        # 注意：这可能会与JavaScript的unescape行为不完全一致，因为JavaScript的unescape不会解码URL编码的字符
        s = urllib.parse.unquote(s)

        return s

    @staticmethod
    def __btoa(data):
        # 确保输入是字节串
        if not isinstance(data, bytes):
            data = data.encode('utf-8')

            # 使用base64编码
        return base64.b64encode(data).decode('utf-8')

    def encode(self, params):
        return self.__btoa(self.__unescape(self.__encode_uri_component(params)))

