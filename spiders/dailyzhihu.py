#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# fileame: dailyzhihu.py

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__),".."))
from lib.spider import *

__all__ = ["dailyzhihuSpider"]


class dailyzhihuSpider(Spider): # 知乎日报

	def __init__(self):
		Spider.__init__(self)
		self.headers = {
			"Host": "daily.zhihu.com",
			"Origin": "https://www.thepaper.cn/",
			"referer": "https://daily.zhihu.com/",
			"upgrade-insecure-requests": "1",
		}

		self.dbTable = "dailyzhihu"
		self.max_workers = 96
		self.workers = 96 # 不反爬虫
		self.Interval_Time = 0
		self.Max_Queue_Size = 5000

	def parse_html(self, html):
		return BeautifulSoup(html,"lxml").find("div","content").text
		
	def get_urls(self):
		maxId = 9687436
		for newsID in range(maxId, 0, -1):
			if self.exists(newsID):
				continue
			else:
				url = "https://daily.zhihu.com/story/%s" % newsID
				yield newsID, url


if __name__ == '__main__':
	spider = dailyzhihuSpider()
	spider.work(loop=True, errs=["ServerError","Null","DecodeError"])