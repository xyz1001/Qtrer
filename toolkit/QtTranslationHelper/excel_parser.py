#!/usr/bin/env python
# -*- coding: utf-8 -*-

import openpyxl
import logging


class ExcelParser(object):
    def __init__(self):
        self.translations = {}

    def parse(self, excel_path):
        book = openpyxl.load_workbook(excel_path)
        sheet = book[book.sheetnames[0]]
        table = tuple(sheet.columns)

        for i in range(0, len(table)):
            if table[i][0].value in self.translations:
                continue
            self.translations[table[i][0].value] = []
            for j in range(1, len(table[0])):
                self.translations[table[i][0].value].append(table[i][j].value)


if __name__ == "__main__":
    excel_parser = ExcelParser()
    excel_parser.parse("tr.xlsx")
