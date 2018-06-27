#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# fileame: thepaper.py

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__),".."))
from lib.spider import *
from lib.spider.error import *

__all__ = ["thepaperSpider"]


class thepaperSpider(Spider): # 澎湃

	def __init__(self):
		Spider.__init__(self)
		self.headers = {
			"Host": "www.thepaper.cn",
			"Origin": "https://www.thepaper.cn/",
		}

		self.dbTable = "thepaper"
		# self.max_worders = 80
		self.workers = 64 # 不反爬虫
		self.Max_Queue_Size = 2000

	def parse_html(self, html):
		soup = BeautifulSoup(html,"lxml").find(class_="news_txt")
		if soup.text == "此文章已下线":
			raise NotFoundError
		else:
			return soup.text

	def get_urls(self):
		maxId = 2211226
		for newsID in range(maxId, 0, -1):
			if self.exists(newsID):
				continue
			else:
				url = "https://www.thepaper.cn/newsDetail_forward_%s" % newsID
				yield newsID, url


if __name__ == '__main__':
	spider = thepaperSpider()
	spider.work(loop=True, errs=["ServerError","Null"])