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
            if table[i][0].value is None:
                continue
            self.translations[table[i][0].value] = []
            for j in range(1, len(table[0])):
                string = table[i][j].value
                if string is None:
                    string = ""
                self.translations[table[i][0].value].append(string)


if __name__ == "__main__":
    excel_parser = ExcelParser()
    excel_parser.parse("tr.xlsx")
