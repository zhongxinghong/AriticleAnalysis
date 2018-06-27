#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# fileame: guokr.py

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__),".."))
from lib.spider import *

__all__ = ["nfpeopleSpider"]


class nfpeopleSpider(Spider): # 南方人物周刊

	def __init__(self):
		Spider.__init__(self)
		self.headers = {
			"Host": "www.nfpeople.com",
			"Origin": "http://www.nfpeople.com/",
		}

		self.dbTable = "nfpeople"
		self.workers = 32

	def parse_html(self, html):
		return BeautifulSoup(html,"lxml").find("div","mainContent").text

	def get_urls(self):
		maxId = 8340
		for newsID in range(maxId, 0, -1):
			if self.exists(newsID):
				continue
			else:
				url = "http://www.nfpeople.com/article/%s" % newsID
				yield newsID, url