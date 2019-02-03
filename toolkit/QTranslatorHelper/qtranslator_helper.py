#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import sys

from excel_parser import ExcelParser
from qt_ts import QtTs
from opencc_translator import OpenccTranslator

# 根据翻译目录下的customer文件夹获取customer列表
def get_customer_list(tr_dir):
    customer_list = []
    for item in os.listdir(tr_dir):
        path = os.path.join(tr_dir, item)
        if os.path.isdir(path):
            customer_list.append(item)
    return customer_list

# 用table_new词条更新替换(或增加到)table词条
def update_tr_table(table, table_new):
    for tr_key in table_new["source"]:
        index_n = table_new["source"].index(tr_key)
        if tr_key in table["source"]:
            index = table["source"].index(tr_key)
            for local_name in table:
                if local_name== "source":
                    continue
                table[local_name][index] = table_new[local_name][index_n]
        else:           
            for local_name in table:
                table[local_name].append(table_new[local_name][index_n])

    return table

# 获得最终翻译的table
def get_tr_table(xlsx_dir, customer):
    tr_table={}
    xlsx_path=""
    for item in os.listdir(xlsx_dir):
        file_path = os.path.join(xlsx_dir, item)
        if os.path.isfile(file_path) and file_path.endswith(".xlsx"):
            xlsx_path = file_path
            break
    
    if xlsx_path == "":
        logging.error("xlsx file not found in directory: %s" % xlsx_dir)
        exit(-1)

    parser = ExcelParser()
    #首先获得public词条
    tr_table_public = parser.parse(xlsx_path, "public")
    tr_table.update(tr_table_public)

    if customer != "public":
        tr_table_customer = parser.parse(xlsx_path, customer)
        # 获取用customer覆盖public词条后的翻译
        tr_table.update(update_tr_table(tr_table, tr_table_customer))
    
    if not tr_table:
        return tr_table

    zh_TW_translator = OpenccTranslator("s2twp")
    tr_table["zh_TW"] = zh_TW_translator.generate(tr_table["zh_CN"])

    zh_HK_translator = OpenccTranslator("s2hk")
    tr_table["zh_HK"] = zh_HK_translator.generate(tr_table["zh_CN"])
    logging.info(tr_table.keys())

    return tr_table

# 将tr_table里的翻译词条写入到ts目录下的所有ts
def tr(ts_dir, tr_table):
    for item in os.listdir(ts_dir):
        ts_path = os.path.join(ts_dir, item)
        if not ts_path.endswith(".ts"):
            continue
        
        # 从每个ts文件命名中获取语言名，由语言名从table中取出对应语言写入ts文件中
        qt_ts = QtTs(ts_path, tr_table)
        locale_name = os.path.splitext(os.path.basename(ts_path))[0]
        print("translating: %s" % ts_path)
        try:
            qt_ts.tr(locale_name)
        except KeyError as e:
            logging.error(e.args)
        qt_ts.save(ts_path)


def tr_all(tr_dir):
    customer_list = get_customer_list(tr_dir)
    for customer in customer_list:
        print("\n%s:" % customer)
        ts_dir = os.path.join(tr_dir, customer)
        tr_table = get_tr_table(tr_dir, customer)
        tr(ts_dir, tr_table)


if __name__ == "__main__":
    if len(sys.argv)<2:
        print("usage:", sys.argv[0],"<project_dir>")
        print("\nMust ensure that translation excel is in \"PROJECT_DIR/doc/translation\", \
\nand qs files in \"PROJECT_DIR/translation\"")
        exit(0)

    project_dir = sys.argv[1]
    tr_dir = project_dir + "/translation"
    tr_all(tr_dir)

    


