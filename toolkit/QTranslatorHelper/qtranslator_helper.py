#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

from excel_parser import ExcelParser
from qt_ts import QtTs
from opencc_translator import OpenccTranslator

if __name__ == "__main__":
    translation_file_dir = input("Input translation file dir: ")
    qt_ts_file_dir = input("input Qt ts file dir: ")

    translation = {}
    for item in os.listdir(translation_file_dir):
        file_path = os.path.join(translation_file_dir, item)
        if not os.path.isfile(file_path) or not file_path.endswith(".xlsx"):
            continue

        parser = ExcelParser()
        parser.parse(file_path)
        translation.update(parser.translations)

    zh_TW_translator = OpenccTranslator("s2twp")
    translation["zh_TW"] = zh_TW_translator.generate(translation["zh_CN"])

    zh_HK_translator = OpenccTranslator("s2hk")
    translation["zh_HK"] = zh_HK_translator.generate(translation["zh_CN"])
    logging.info(translation.keys())

    for item in os.listdir(qt_ts_file_dir):
        file_path = os.path.join(qt_ts_file_dir, item)
        if not file_path.endswith(".ts"):
            continue

        qt_ts = QtTs(file_path)
        locale_name = os.path.splitext(os.path.basename(file_path))[0]
        qt_ts.set_target_language(locale_name)
        try:
            qt_ts.translate(translation)
        except KeyError as e:
            logging.error(e.args)
        qt_ts.save(file_path)

    os.system("lrelease %s/*.ts" % qt_ts_file_dir)
