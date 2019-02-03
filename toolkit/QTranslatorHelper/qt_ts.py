#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ElementTree
import logging


class QtTs(object):
    def __init__(self, ts_path, tr_table):
        self.ts_path = ts_path
        self.xml_tree = ElementTree.parse(ts_path)
        self.tr_table = tr_table

    def __get_tr_list(self, locale_name):
        if locale_name in self.tr_table:
            return self.tr_table[locale_name]
        else:
            return []

    def __get_target_tr_list(self, locale_name):
        logging.info("target locale name: %s" %locale_name)
        tr_list = self.__get_tr_list(locale_name)
        if tr_list:
            return tr_list

        language_name = locale_name[0:2]
        for key in self.tr_table.keys():
            if key.startswith(language_name):
                logging.info("Found transltion %s" % key)
                return self.tr_table[key]

        logging.error("Fail to translate to %s",
                      locale_name)
        raise KeyError("%s: Target translation NOT found" %
                       locale_name)

    def __get_tr(self, source_string, source_tr_list, target_tr_list):
        try:
            index = source_tr_list.index(source_string)
            return target_tr_list[index]
        except (ValueError, IndexError):
            logging.error("no source string '%s' found" % source_string)

    def tr(self, locale_name):
        root = self.xml_tree.getroot()
        source_tr_list = self.__get_tr_list("source")
        if not source_tr_list:
             logging.error("no source list found")
             exit(-1)
        target_tr_list = self.__get_target_tr_list(locale_name)
        en_tr_list = self.__get_target_tr_list("en")
        for context in root:
            for message in context:
                if message.tag != "message":
                    continue
                source = message.find("source")
                target_string = self.__get_tr(
                    source.text, source_tr_list, target_tr_list)
                if target_string is None:
                    continue
                if target_string.strip() == "":                 #若翻译词条为空，使用英文翻译
                    target_string = self.__get_tr(
                    source.text, source_tr_list, en_tr_list)

                translation = message.find("translation")
                translation.attrib.clear()
                translation.text = target_string
                logging.info("translate %s to %s" %
                             (source.text, translation.text))

    def save(self, path):
        self.xml_tree.write(path, encoding="utf-8",
                            xml_declaration=True)
        with open(path, "r+") as file:
            contents = file.readlines()
            contents.insert(1, "<!DOCTYPE TS>\n")
            file.seek(0)
            file.writelines(contents)


if __name__ == "__main__":
    ts = QtTs("./zh_CN.ts")
    ts.set_target_language("zh", "CN")
    ts.save()
