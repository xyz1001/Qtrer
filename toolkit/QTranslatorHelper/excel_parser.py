#!/usr/bin/env python
# -*- coding: utf-8 -*-

import openpyxl
import logging


class ExcelParser(object):
    def parse(self, excel_path, customer):
        translations = {}
        book = openpyxl.load_workbook(excel_path)
        all_sheet = book.get_sheet_names()
        if customer not in all_sheet:
            print("customer %s not in %s" % (customer, excel_path))
            return translations

        sheet = book[customer]
        table = tuple(sheet.columns)

        for i in range(0, len(table)):
            if table[i][0].value in translations:
                continue
            if table[i][0].value is None:
                continue
            translations[table[i][0].value] = []
            for j in range(1, len(table[0])):
                string = table[i][j].value
                if string is None:
                    string = ""
                translations[table[i][0].value].append(string)
        return translations


if __name__ == "__main__":
    excel_parser = ExcelParser()
    excel_parser.parse("tr.xlsx")
