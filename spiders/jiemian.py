#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# fileame: jiemian.py
# 

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__),".."))
from lib.spider import *


__all__ = ["jiemianSpider"]


class jiemianSpider(Spider): # 界面

	def __init__(self):
		Spider.__init__(self)
		self.headers = {
			"Host": "www.jiemian.com",
			"Origin": "http://www.jiemian.com/",
		}

		self.dbTable = "jiemian"
		self.workers = 32 # 反爬虫，会伪造请求失败！
		self.Allow_Redirects = False
		self.Interval_Time = 0
		self.Max_Queue_Size = 2000

	def parse_html(self, html):
		return BeautifulSoup(html,"lxml").find("div","article-content").text

	def get_urls(self):
		maxId = 2248950

		for newsID in range(maxId, 0, -1):
			if self.exists(newsID):
				continue
			else:
				url = "http://www.jiemian.com/article/%s.html" % newsID
				yield newsID, url


if __name__ == '__main__':
	spider = jiemianSpider()
	spider.work(loop=True, errs=["ServerError","Null","DecodeError"])