#!/usr/bin/env python
# -*- coding: utf-8 -*-

from excel_parser import ExcelParser
from qt_ts import QtTs
from opencc_translator import OpenccTranslator

if __name__ == "__main__":
    parser = ExcelParser()
    parser.parse("./tr/MaxhubAirClient.xlsx")

    translations = parser.translations
    zh_TW_translator = OpenccTranslator("s2twp")
    translations["zh_TW"] = zh_TW_translator.generate(translations["zh_CN"])

    zh_HK_translator = OpenccTranslator("s2hk")
    translations["zh_HK"] = zh_HK_translator.generate(translations["zh_CN"])

    zh_CN_ts = QtTs("./raw/zh_CN.ts")
    zh_CN_ts.set_target_language("zh", "CN")
    zh_CN_ts.translate(parser.translations)
    zh_CN_ts.save("./ok/zh_CN.ts")
    print("")

    zh_TW_ts = QtTs("./raw/zh_TW.ts")
    zh_TW_ts.set_target_language("zh", "TW")
    zh_TW_ts.translate(parser.translations)
    zh_TW_ts.save("./ok/zh_TW.ts")
    print("")

    zh_HK_ts = QtTs("./raw/zh_HK.ts")
    zh_HK_ts.set_target_language("zh", "HK")
    zh_HK_ts.translate(parser.translations)
    zh_HK_ts.save("./ok/zh_HK.ts")
    print("")

    de_ts = QtTs("./raw/de.ts")
    de_ts.set_target_language("de")
    de_ts.translate(parser.translations)
    de_ts.save("./ok/de.ts")
    print("")

    es_ts = QtTs("./raw/es.ts")
    es_ts.set_target_language("es")
    es_ts.translate(parser.translations)
    es_ts.save("./ok/es.ts")
    print("")

    fr_ts = QtTs("./raw/fr.ts")
    fr_ts.set_target_language("fr")
    fr_ts.translate(parser.translations)
    fr_ts.save("./ok/fr.ts")
    print("")

    it_ts = QtTs("./raw/it.ts")
    it_ts.set_target_language("it")
    it_ts.translate(parser.translations)
    it_ts.save("./ok/it.ts")
    print("")

    ja_ts = QtTs("./raw/ja.ts")
    ja_ts.set_target_language("ja")
    ja_ts.translate(parser.translations)
    ja_ts.save("./ok/ja.ts")
    print("")

    ko_ts = QtTs("./raw/ko.ts")
    ko_ts.set_target_language("ko", "KR")
    ko_ts.translate(parser.translations)
    ko_ts.save("./ok/ko.ts")
    print("")

    pt_ts = QtTs("./raw/pt.ts")
    pt_ts.set_target_language("pt")
    pt_ts.translate(parser.translations)
    pt_ts.save("./ok/pt.ts")
    print("")

    ru_ts = QtTs("./raw/ru.ts")
    ru_ts.set_target_language("ru")
    ru_ts.translate(parser.translations)
    ru_ts.save("./ok/ru.ts")
    print("")
