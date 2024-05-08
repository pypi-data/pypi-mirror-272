# -*- coding: utf-8 -*- 
"""
Author: JerryLaw
Time: 2023/11/12 19:11
File: debugTalk.py
Email: 623487850@qq.com
"""

from common.paramsEncoder import Encoder


class DebugTalk:
    def encodeParams(self, param):
        return Encoder().encode(param)

