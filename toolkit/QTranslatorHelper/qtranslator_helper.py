#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import sys

from excel_parser import ExcelParser
from qt_ts import QtTs
from opencc_translator import OpenccTranslator

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("usage:", sys.argv[0],"<project_dir>")
        print("\nMust ensure that translation excel is in \"PROJECT_DIR/doc/translation\", \
\nand qs files in \"PROJECT_DIR/translation\"")
        exit(0)

    project_dir = sys.argv[1]
    translation_file_dir = project_dir + "/doc/translation"
    qt_ts_file_dir = project_dir + "/translation"

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
