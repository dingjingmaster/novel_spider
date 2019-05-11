#!/usr/bin/env python
# -*- encoding=utf8 -*-

import re
import os
import base64
import hashlib
from frame.log.log import log as logging


class NovelBean:
	def __init__(self):
		self._bookUrl = ''                          # 书籍 url ok
		self._imgUrl = ''                           # 书籍封面 img  ok
		self._chapterBaseURL = ''                   # 章节url  no
		self._name = ''                             # 书籍名字 ok
		self._author = ''                           # 书籍作者 ok
		self._category = ''                         # 书籍分类 ok
		self._imgContent = None                     # 书籍图片 ok
		self._chapterIndex = {}                     # 书籍章节 url 和 顺序
		self._chapters = {}                         # 书籍 url 和 章节名 以url为key
		self._content = {}                          # 书籍 url 和 内容名
		self._imgLocal = ''                         # 图片的本地路径
		self._desc = ''                             # 描述 ok
		self._status = ''                           # 连载状态 ok

	class NovelInfo:
		def __init__(self):
			pass








	def saveInfo(self, path: str):
		if (self._name == "") or (len(self._chapters) != len(self._chapterIndex)):
			logging.error(self._bookUrl + '书名为空')
			return None
		logging.info(self._name + ' - ' + self._author + ' 开始保存...')
		bookDir = path + '/' + self._encode(self._bookUrl) + '/'
		# 创建书籍文件夹
		if not os.path.exists(bookDir):
			os.mkdir(bookDir)

		# 章节信息
		chapter = ''
		if len(self._chapters) > 0:
			for ik, iv in self._chapters.items():
				chapter += ik + '|' + iv + '{]'
		if '' != chapter:
			chapter = chapter[: -2]

		chapterIndex = ''
		if len(self._chapterIndex) > 0:
			for ik, iv in self._chapterIndex.items():
				chapterIndex += ik + '|' + str(iv) + '{]'
		if '' != chapterIndex:
			chapterIndex = chapterIndex[:-2]
			
		# 保存图片
		k = ''
		arr = self._imgUrl.split('.')
		if len(arr) >= 2:
			k = arr[len(arr) - 1]
		if None is not self._imgContent:
			with open(bookDir + self._name + '.' + k, 'wb') as fw:
				fw.write(self._imgContent)

		# 保存章节内容
		if len(self._chapters) > 0:
			for ik, iv in self._chapters.items():
				with open(bookDir + self._encode(ik) + '.txt', 'w', encoding='utf8') as fw:
					fw.write(self._content[ik].strip())
		# 保存摘要
		with open(bookDir + 'index.txt', 'w', encoding='utf8') as fw:
			fw.write('bookURL:' + self._bookUrl + '\n')
			fw.write('imgURL:' + self._imgUrl + '\n')
			fw.write('chapterURL:' + self._chapterBaseURL + '\n')
			fw.write('name:' + self._name + '\n')
			fw.write('author:' + self._author + '\n')
			fw.write('desc:' + self._desc + '\n')
			fw.write('status:' + self._status + '\n')
			fw.write('category:' + self._category + '\n')
			fw.write('chapter:' + chapter + '\n')
			fw.write('imageLocal:' + bookDir + self._name + '.' + k + '\n')
			fw.write('chapterIndex:' + chapterIndex + '\n')
		logging.info(self._name + ' - ' + self._author + ' 保存完成!!!')

	def getInfo(self, noveldir: str):
		self._bookUrl = ''
		self._imgUrl = ''
		self._chapterBaseURL = ''
		self._name = ''
		self._author = ''
		self._category = ''
		self._desc = ''
		self._imgContent = None
		self._chapterIndex = {}
		self._chapters = {}
		self._content = {}
		self._imgLocal = ''
		self._status = '连载'

		# 获取图片信息
		for d in os.listdir(noveldir):
			if re.search(r'.(png|jpg|bmp|jpeg|gif)$', d, re.I | re.U):
				self._imgLocal = noveldir + '/' + d

		if not os.path.exists(noveldir + '/index.txt'):
			return None

		# 获取信息
		chapter = ''
		chapterIndex = ''
		with open(noveldir + '/index.txt', 'r', encoding='utf8') as fr:
			for line in fr.readlines():
				line = line.strip('\n')
				arr = line.split(':')
				key = ''
				val = ''
				if len(arr) >= 2:
					key = arr[0]
					val = ':'.join(arr[1:])
				if 'bookURL' == key:
					self._bookUrl = val
				elif 'imgURL' == key:
					self._imgUrl = val
				elif 'chapterURL' == key:
					self._chapterBaseURL = val
				elif 'name' == key:
					self._name = val
				elif 'author' == key:
					self._author = val
				elif 'category' == key:
					self._category = val
				elif 'chapter' == key:
					chapter = val
				elif 'chapterIndex' == key:
					chapterIndex = val
				elif 'desc' == key:
					self._desc = val
				elif 'imageLocal' == key:
					self._imgLocal = val
				elif 'status' == key:
					self._status = val
		# 章节名和章节 url 解析
		arr = chapter.split('{]')
		if len(arr) <= 0:
			return None
		for line in arr:
			aa = line.split('|')
			if len(aa) <= 1:
				return None
			self._chapters[aa[0]] = aa[1]
		arr = chapterIndex.split('{]')
		if len(arr) <= 0:
			return None
		for line in arr:
			aa = line.split('|')
			if len(aa) <= 1:
				return None
			self._chapterIndex[aa[0]] = aa[1]
		# 获取章节内容
		if len(self._chapterIndex) != len(self._chapters):
			return None
		for url, iv in self._chapters.items():
			ct = ''
			with open(noveldir + '/' + self._encode(url) + '.txt', 'r', encoding='utf8') as fr:
				for i in fr.readlines():
					i = i.strip()
					ct += '<p>&nbsp;&nbsp;' + i + '</p>'
			self._content[url] = ct
		if len(self._chapterIndex) != len(self._content):
			return None
		return self

	def setBookURL(self, url):
		if None is not url:
			self._bookUrl = url
		return self

	def getBookURL(self):
		return self._bookUrl

	def setChapterURL(self, url):
		if None is not url:
			self._chapterBaseURL = url
		return self

	def getChapterURL(self):
		return self._chapterBaseURL

	def chapterExit(self, path: str, chapterURL: str)->bool:
		bookDir = path + '/' + self._encode(self._bookUrl) + '/' + self._encode(chapterURL)
		return os.path.exists(bookDir)

	def imageExit(self, path: str):
		k = ''
		arr = self._imgUrl.split('.')
		if len(arr) >= 2:
			k = arr[len(arr) - 1]
		return os.path.exists(path + '/' + self._encode(self._bookUrl) + '/' + self._name + k)

	def setName(self, name):
		if None is not name:
			self._name = normName(name)
		return self

	def getName(self):
		return self._name

	def setAuthor(self, author):
		if None is not author:
			self._author = normAuthor(author)
		return self

	def getAuthor(self):
		return self._author

	def setCategory(self, cate):
		if None is not cate:
			arr = cate.split(']')
			cate = arr[0]
			arr = cate.split('[')
			if len(arr) >= 2:
				cate = arr[1]
			self._category = normTag(cate)
		return self

	def getCategory(self):
		return self._category

	def setImgUrl(self, url: str):
		if None is not url:
			self._imgUrl = url
		return self

	def getImgUrl(self):
		return self._imgUrl

	def getImgeLocal(self):
		base, name = os.path.split(self._imgLocal)
		return name, self._imgLocal

	def setChapter(self, index, name, url, content):
		if '' == url or None is url:
			return self
		self._chapterIndex[url] = index
		self._chapters[url] = normName(name)
		self._content[url] = content
		return self

	def getChapter(self):
		return self._chapterIndex, self._chapters, self._content

	def setImgContent(self, content):
		if None is not content:
			self._imgContent = content
		return self

	def setDesc (self, desc):
		self._desc = desc

	def getDesc(self):
		return self._desc

	def setStatus(self, status: str):
		if re.search(r'(完结|完成|结束|大结局|完本|完|结)', status):
			self._status = '完结'
		else:
			self._status = '连载'

	def getStatus(self):
		return self._status

	def _encode(self, name: str)->str:
		if None is name or '' == name:
			return ''
		m2 = hashlib.md5()
		m2.update(base64.b64encode(name.encode('utf8')))
		return m2.hexdigest()


def normName(name: str) ->str:
	# 去掉所有非法字符
	name = re.sub(r'[\\/:*?"<>|.]', '', name)
	if None is name:
		name = ''
	return name


def normAuthor(author: str) ->str:
	author = re.sub(r'[\\/:*?"<>|.]', '', author)
	if author is None:
		author = ''
	return author


def normTag(tag: str) ->str:
	tag = re.sub(r'[\\/:*?"<>|.\[\]]', '', tag)
	if tag is None:
		tag = ''
	return tag


def ifExit(path)-> bool:
	return os.path.exists(path)


""" 分类获取 """
# categoryDict = {
# 	'玄幻': 100,                      # 玄幻奇幻
# 	'玄幻小说': 100,                    # 玄幻小说
# 	'武侠': 101,                      # 武侠仙侠
# 	'历史': 102,                      # 历史军事
# 	'现代': 103,                      # 现代都市
# 	'科幻': 104,                      # 科幻小说
# 	'105': 105,                      # 灵异悬疑
# 	'106': 106,                      # 游戏竞技
# 	'107': 107,                      # 二次元
# 	'言情': 200,                     # 现代言情
# 	'201': 201,                     # 古代言情
# 	'202': 202,                     # 幻想言情
# 	'203': 203,                     # 女生悬疑
# 	'同人': 204,                    # 同人小说
# 	'耽美': 205,                    # 青春耽美
# }


# def getCategoryNum(cate: str)->int:
# 	category = 109
# 	if cate in categoryDict.keys():
# 		category = categoryDict[cate]
# 	return category
#
