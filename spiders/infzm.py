#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# fileame: infzm.py

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__),".."))
from lib.spider import *

__all__ = ["infzmSpider"]


class infzmSpider(Spider): # 南方周末

	def __init__(self):
		Spider.__init__(self)
		self.headers = {
			"Host": "passport.infzm.com",
			"Origin": "http://www.infzm.com",
		}

		self.dbTable = "infzm"
		self.max_workers = 48
		self.workers = 32 # 反爬虫 ！
		#self.Allow_Redirects = False
		

	def parse_html(self, html):
		# 注意！ 302 的情况为 NotFound 进一步补充
		return BeautifulSoup(html,"lxml").find(id="articleContent").text

	def get_urls(self):
		maxId = 136700
		for newsID in range(maxId ,0, -1):
			if self.exists(newsID):
				continue
			else:
				url = "http://www.infzm.com/content/%s" % newsID
				yield newsID, url


if __name__ == '__main__':
	spider = infzmSpider()
	spider.work()
