#!/usr/bin/env python3.6
# -*-encoding=utf8-*-
import time
import pyquery
import requests
from fake_useragent import UserAgent
from frame.log.log import log


class Get:
	def __init__(self, url: str, try_time=9, try_sec=2):
		ua = UserAgent()
		self._url = url
		self._try_time = try_time
		self._try_sec = try_sec
		self._header = {
			'User-Agent': ua.ie,
			'Accept-Encoding': ', '.join(('gzip', 'deflate')),
			'Accept': '*/*',
			'Connection': 'keep-alive',
		}

	def html(self)-> str:
		tm = 0
		text = ''
		retry = 1
		while tm <= self._try_time:
			try:
				s = requests.Session()
				
				r = s.get(self._url, headers=self._header)
				if r.status_code == requests.codes.ok:
					doc = pyquery.PyQuery(r.text.encode(r.encoding))
					text = doc.html()
					break
				s.close()
			except Exception:
				log.warning(self._url + '重试:' + str(retry))
				retry += 1
				time.sleep(self._try_sec)
			tm += 1
		return text

	def binary(self):
		tm = 0
		binary = None
		retry = 1
		while tm <= self._try_time:
			try:
				s = requests.Session()
				r = s.get(self._url)
				if r.status_code == requests.codes.ok:
					binary = r.content
					if None is not binary:
						break
					break
				s.close()
			except Exception:
				log.warning(self._url + '重试:' + str(retry))
				retry += 1
				time.sleep(self._try_sec)
			tm += 1
		return binary


