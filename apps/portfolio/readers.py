import os
import zipfile

import pandas
from django.utils.functional import cached_property
from pyxlsb import open_workbook as open_xlsb_workbook
from xlrd import open_workbook as open_xlsx_workbook

from apps.portfolio.exceptions import (BadFormat, EmptyFileException,
                                       NotRecognizedExtension)


def create_reader(file_path: str) -> type:
    file_extension = file_path.split('.')[-1]
    if file_extension == 'xlsx':
        return XLSXPortfolioReader(file_path=file_path)
    elif file_extension == 'xlsb':
        return XLSBPortfolioReader(file_path=file_path)
    elif file_extension == 'csv':
        return CSVPortfolioReader(file_path=file_path)
    else:
        raise NotRecognizedExtension()


class PortfolioReader(object):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        if os.stat(file_path).st_size == 0:
            raise EmptyFileException()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        raise NotImplementedError

    @cached_property
    def workbook(self):
        return self.open_workbook()

    def open_workbook(self):
        raise NotImplementedError

    def get_schema(self):
        schema = {}
        for sheet_name in self.get_sheet_names():
            schema[sheet_name] = self.get_column_names(sheet_name)
        return schema

    def get_sheet_names(self):
        raise NotImplementedError

    def get_column_names(self, sheet_name):
        """
        Returns a list of tuples containing [(index, name), ...]
        """
        data_frame = self._get_data_frame(sheet_name)
        columns = []

        for column_index, column_name in enumerate(data_frame.columns):
            column = data_frame.iloc[:, [column_index]]
            if int(column.isnull().sum()) < len(column):
                columns.append((column_index, column_name))

        return columns

    def get_data_frame(self, sheet_name, column_indexes):
        data_frame = self._get_data_frame(sheet_name)
        return data_frame.iloc[:, column_indexes]

    def _get_data_frame(self, sheet_name):
        raise NotImplementedError


class XLSXPortfolioReader(PortfolioReader):

    def open_workbook(self):
        try:
            return open_xlsx_workbook(
                self.file_path,
                on_demand=True
            )
        except zipfile.BadZipFile:
            raise BadFormat()

    def get_sheet_names(self):
        return self.workbook.sheet_names()

    def _get_data_frame(self, sheet_name):
        data_frame = pandas.read_excel(
            io=self.workbook,
            sheet_name=sheet_name,
            dtype=str,
            engine='xlrd')
        return data_frame

    def __exit__(self, type, value, traceback):
        if self.workbook:
            self.workbook.release_resources()


class XLSBPortfolioReader(PortfolioReader):

    def open_workbook(self):
        try:
            return open_xlsb_workbook(self.file_path)
        except zipfile.BadZipFile:
            raise BadFormat()

    def get_sheet_names(self):
        return self.workbook.sheets

    def _get_data_frame(self, sheet_name):
        lines = []
        with self.workbook.get_sheet(sheet_name) as sheet:
            for row in sheet.rows():
                lines.append([item.v for item in row])
        data_frame = pandas.DataFrame(lines[1:], columns=lines[0] or None)
        return data_frame

    def __exit__(self, type, value, traceback):
        if self.workbook:
            self.workbook.close()


class CSVPortfolioReader(PortfolioReader):
    pass
