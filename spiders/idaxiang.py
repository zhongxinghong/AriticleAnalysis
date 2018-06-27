#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# fileame: idaxiang.py
# 

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__),".."))

cachedir = os.path.join(os.path.dirname(__file__),"../cache/")
urlsFile = os.path.join(cachedir,"idaxiang_urls.json")

from lib.util.utilfuncs import show_status, iter_split
from lib.spider import *
from lib.spider.error import *

import json
import re


__all__ = ["idaxiangSpider"]


class idaxiangSpider(Spider): # 三联生活周刊

	def __init__(self):
		Spider.__init__(self)
		self.headers = {
			"Host": "wemedia.ifeng.com",
		}

		self.dbTable = "idaxiang"
		self.workers = 8 # 请求频率不能过高
		self.Auto_Speed_Up = False
		self.Allow_Redirects = False # 重定向至凤凰网首页
		self.Interval_Time = 0
		self.Max_Queue_Size = 100

		#self.Response_Charset = ["utf-8","gbk","gb2312",None]


	def pre_get_urls(self):
		self.Use_Proxy = False
		#self.Allow_Redirects = True

		try:
			urls = ["http://wemedia.ifeng.com/zhengming/7927_%s/list.shtml" % page for page in range(1,31+1)]
			newsUrl = []
			for url in show_status(urls):
				try:
					html = self.get(url)
				except NotFoundError:
					print(url)
					continue
				bodySoup = BeautifulSoup(html,"lxml")
				for ulSoup in bodySoup.find_all("ul","listNews"):
					for txtdiv in ulSoup.find_all("div","txt"):
						newsUrl.append(txtdiv.find("h2").find("a").get("href",None))
		except KeyboardInterrupt as err:
			pass
		except Exception as err:
			print(repr(err))
			#raise err
		finally:
			with open(urlsFile,"w") as fp:
				fp.write(json.dumps(newsUrl))

	def get_urls(self):
		with open(urlsFile,"r") as fp:
			urls = json.loads(fp.read())
			urls = list(set([url for url in urls if url]))

		reID = re.compile(r"^http://wemedia.ifeng.com/(\d+)/wemedia.shtml$")
		for url in urls:
			newsID = reID.match(url)
			if newsID:
				newsID = int(newsID.group(1))
				if not self.exists(newsID):
					yield newsID, url
			else:
				print(url)

	def parse_html(self, html):
		return BeautifulSoup(html,"lxml").find(id="txtBox").text

if __name__ == '__main__':
	spider = idaxiangSpider()
	#spider.pre_get_urls()
	#a = [x for x in spider.get_urls()]
	#spider.trial()
	spider.work(loop=True, errs=["ServerError","NotFound","Null","EmptyPage","DecodeError"])
