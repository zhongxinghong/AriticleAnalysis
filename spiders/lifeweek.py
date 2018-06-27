#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# fileame: lifeweek.py
# 

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__),".."))

cachedir = os.path.join(os.path.dirname(__file__),"../cache/")
urlsFile = os.path.join(cachedir,"lifeweek_urls.json")

from lib.util.utilfuncs import show_status, iter_split
from lib.spider import *
from lib.spider.error import *

import json
import re


__all__ = ["lifeweekSpider"]


class lifeweekSpider(Spider): # 三联生活周刊

	def __init__(self):
		Spider.__init__(self)
		self.headers = {
			"Host": "www.lifeweek.com.cn",
			"Referer": "http://www.lifeweek.com.cn/",
		}

		self.dbTable = "lifeweek"
		self.workers = 16
		self.Auto_Speed_Up = False
		self.Allow_Redirects = True 
		self.Interval_Time = 0
		self.Max_Queue_Size = 100

		self.Response_Charset = ["utf-8","gbk","gb2312",None]


	def pre_get_urls(self):
		self.Use_Proxy = False
		#self.Allow_Redirects = True

		try:
			urls = ["http://www.lifeweek.com.cn/story/%s.shtml" % page for page in range(1,318+1)]
			newsUrl = []
			for url in show_status(urls):
				try:
					html = self.get(url)
				except NotFoundError:
					print(url)
					continue
				bodySoup = BeautifulSoup(html,"lxml")
				for ulSoup in bodySoup.find_all("ul","contentlist"):
					for a in ulSoup.find_all("a","caption"):
						newsUrl.append(a.get("href",None))
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

		reID = re.compile(r"^http://www.lifeweek.com.cn/(\d{4})/(\d{4})/(\d+).shtml$")
		for url in urls:
			newsID = reID.match(url)
			if newsID:
				newsID = int("".join(newsID.group(1,2,3)))
				if not self.exists(newsID):
					yield newsID, url
			else:
				print(url)

	def parse_html(self, html):
		return " ".join([p.text for p in BeautifulSoup(html,"lxml").find("article").find_all("p")])

if __name__ == '__main__':
	spider = lifeweekSpider()
	#spider.pre_get_urls()
	#spider.trial()
	spider.work(loop=True, errs=["ServerError","NotFound","EmptyPage","Null","DecodeError"])
