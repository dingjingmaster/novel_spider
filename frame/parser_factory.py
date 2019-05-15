#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
from frame.common.param import *
from frame.novel_parser.ccuu234 import CCuu234Parser


class ParserFactory:
    def get_parser(self, parser_name: str):
        if parser_name in self._parserDict:
            return self._parserDict[parser_name]
    _parserDict = {
        CC_UU234_NAME: CCuu234Parser(),
    }


_parser = ParserFactory()


def get_parser():
    return _parser
