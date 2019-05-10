#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
from frame.novel_parser.feidu_parser import FeiduParser


class ParserFactory:
    def get_parser(self, parser_name: str):
        if parser_name in self._parserDict:
            return self._parserDict[parser_name]
    _parserDict = {
        '34fd_com': FeiduParser(),
    }


if __name__ == '__main__':
    parser = ParserFactory()
    feidu = parser.get_parser('34fd_com')
    exit(0)
