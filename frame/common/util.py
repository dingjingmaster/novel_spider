#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
from urllib.parse import unquote


class Util:
    @staticmethod
    def check_url(url: str, base_url: str) -> str:
        if not url.startswith("https://") and url.startswith("http://"):
            url = base_url + '/' + url
        try:
            url = unquote(url, 'utf8')
        except Exception:
            url = ''
        return url
