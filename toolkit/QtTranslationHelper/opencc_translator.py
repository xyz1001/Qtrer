#!/usr/bin/env python
# -*- coding: utf-8 -*-

from opencc import OpenCC


class OpenccTranslator(object):
    def __init__(self, config):
        self.opencc = OpenCC(config)
        self.target_strings = []

    def generate(self, chs_strings):
        for string in chs_strings:
            self.target_strings.append(self.opencc.convert(string))
        return self.target_strings


if __name__ == "__main__":
    strings = ["软件", "对象", "中文"]
    translator = OpenccTranslator("s2hk")
    print(translator.generate(strings))
