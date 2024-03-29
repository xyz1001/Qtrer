#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Translate Qt ts file

Usage:
    qtrer [--ts_dir=<ts_dir> --excel_dir=<excel_dir> --log_level=<log_level> --patch]

Options:
    --ts_dir=<ts_dir>                       Qt翻译文件的目录
    --excel_dir=<excel_dir>                 Excel翻译文件的路径
    --loglevel=<log_level>                  log等级：NOTSET,DEBUG,INFO,WARN,ERROR,FATAL,CRITICAL
    --patch                                 补丁翻译模式
"""

import os
import logging
import sys
import docopt
import pandas

from excel_parser import ExcelParser
from qt_ts import QtTs
from opencc_translator import OpenccTranslator


def main():
    arg = docopt.docopt(__doc__)
    qt_ts_file_dir = arg["--ts_dir"]
    translation_file_dir = arg["--excel_dir"]
    log_level = arg["--log_level"]

    if qt_ts_file_dir is None:
        qt_ts_file_dir = "./translation"
    if translation_file_dir is None:
        translation_file_dir = "./doc/translation"
    if log_level is None:
        log_level = "INFO"

    logging.basicConfig(level=logging._nameToLevel[log_level.upper()])

    translation = {}
    for item in os.listdir(translation_file_dir):
        file_path = os.path.join(translation_file_dir, item)
        if not os.path.isfile(file_path) or not (file_path.endswith(".xlsx") or file_path.endswith(".csv")):
            continue

        temp_falg = False
        if file_path.endswith(".csv"):
            read_file = pandas.read_csv(file_path)
            file_path = './__temp.xlsx'
            read_file.to_excel(file_path, index=None, header=True)
            temp_falg = True

        parser = ExcelParser()
        parser.parse(file_path)
        translation.update(parser.translations)
        if temp_falg:
            os.remove(file_path)

    if "zh_TW" not in translation:
        logging.info("zh_TW not in doc, use OpenccTranslator")
        zh_TW_translator = OpenccTranslator("s2twp")
        translation["zh_TW"] = zh_TW_translator.generate(translation["zh_CN"])

    if "zh_HK" not in translation:
        logging.info("zh_HK not in doc, use OpenccTranslator")
        zh_HK_translator = OpenccTranslator("s2hk")
        translation["zh_HK"] = zh_HK_translator.generate(translation["zh_CN"])
    logging.info(translation.keys())

    for item in os.listdir(qt_ts_file_dir):
        file_path = os.path.join(qt_ts_file_dir, item)
        if not file_path.endswith(".ts"):
            continue

        qt_ts = QtTs(file_path, translation, arg["--patch"])
        locale_name = os.path.splitext(os.path.basename(file_path))[0]
        try:
            qt_ts.tr(locale_name)
        except KeyError as e:
            logging.error(e.args)
            raise
        qt_ts.save(file_path)


if __name__ == "__main__":
    main()
