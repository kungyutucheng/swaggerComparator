# -*- coding: UTF-8 -*-
import sys
sys.path.append('..')
from enums.ActualDataType import ActualDataType
from enums.DataFormat import DataFormat
from enums.ShowDataType import ShowDataType

reload(sys)
sys.setdefaultencoding('utf8')


class TypeConvertor(object):

    @staticmethod
    def convertToActualDataType(type, format):
        if type == ShowDataType.INTEGER and format == DataFormat.INT32:
            return ActualDataType.INTEGER
        elif type == ShowDataType.INTEGER and format == DataFormat.INT64:
            return ActualDataType.LONG
        elif type == ShowDataType.NUMBER and format == DataFormat.FLOAT:
            return ActualDataType.FLOAT
        elif type == ShowDataType.NUMBER and format == DataFormat.DOUBLE:
            return ActualDataType.DOUBLE
        elif type == ShowDataType.STRING and format is None:
            return ActualDataType.STRING
        elif type == ShowDataType.STRING and format == DataFormat.BYTE:
            return ActualDataType.BYTE
        elif type == ShowDataType.STRING and format == DataFormat.BINARY:
            return ActualDataType.BINARY
        elif type == ShowDataType.BOOLEAN and format is None:
            return ActualDataType.BOOLEAN
        elif type == ShowDataType.STRING and format == DataFormat.DATE:
            return ActualDataType.DATE
        elif type == ShowDataType.STRING and format == DataFormat.DATE_TIME:
            return ActualDataType.DATE_TIME
        elif type == ShowDataType.STRING and format == DataFormat.PASSWORD:
            return ActualDataType.PASSWORD
        elif type == ShowDataType.OBJECT and format is None:
            return ActualDataType.OBJECT
        elif type == ShowDataType.ARRAY and format is None:
            return ActualDataType.ARRAY
        return None