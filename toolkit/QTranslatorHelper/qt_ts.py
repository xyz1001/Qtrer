#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ElementTree
import logging


class QtTs(object):
    def __init__(self, ts_path):
        self.ts_path = ts_path
        self.xml_tree = ElementTree.parse(ts_path)
        self.target_locale_name = ""

    def set_target_language(self, locale_name):
        self.target_locale_name = locale_name
        root = self.xml_tree.getroot()
        root.attrib["language"] = self.target_locale_name

    def __get_source_strings(self, translation_table):
        if "source" in translation_table:
            return translation_table["source"]
        else:
            logging.critical("No EN language translation found")
            exit(-1)

    def __get_target_strings(self, translation_table):
        logging.info("target locale name: %s" %
                     (self.target_locale_name))
        if self.target_locale_name in translation_table:
            logging.info("Found transltion %s" % self.target_locale_name)
            return translation_table[self.target_locale_name]

        language_name = self.target_locale_name[0:2]
        for key in translation_table.keys():
            if key.startswith(language_name):
                logging.info("Found transltion %s" % key)
                return translation_table[key]

        logging.error("Fail to translate to %s",
                      self.target_locale_name)
        raise KeyError("%s: Target translation NOT found" %
                       self.target_locale_name)

    def __get_translation(self, source_string, source_strings, target_strings):
        try:
            index = source_strings.index(source_string)
            return target_strings[index]
        except (ValueError, IndexError):
            logging.error("no source string '%s' found" % source_string)

    def translate(self, translation_table):
        root = self.xml_tree.getroot()
        source_strings = self.__get_source_strings(translation_table)
        target_strings = self.__get_target_strings(translation_table)
        for context in root:
            for message in context:
                if message.tag != "message":
                    continue
                source = message.find("source")
                target_string = self.__get_translation(
                    source.text, source_strings, target_strings)
                if target_string is None:
                    continue

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
