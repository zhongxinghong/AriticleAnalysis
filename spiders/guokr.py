#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# fileame: guokr.py

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__),".."))
from lib.spider import *

__all__ = ["guokrSpider"]


class guokrSpider(Spider): # 果壳

	def __init__(self):
		Spider.__init__(self)
		self.headers = {
			"Host": "www.guokr.com",
			"Origin": "https://www.guokr.com/",
			"Cookie": "BAIDU_SSP_lcr=https://www.google.com.hk/; __utmt=1; __utma=253067679.1955159427.1526885538.1526885538.1529650330.2; __utmb=253067679.39.9.1529650504362; __utmc=253067679; __utmz=253067679.1529650330.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=253067679.|1=Is%20Registered=No=1",
			"Upgrade-Insecure-Requests": "1",
			"Connection": "keep-alive",
		}
		
		self.dbTable = "guokr"
		self.workers = 2
		self.Auto_Speed_Up = False # 服务器好像不行 ？

	def parse_html(self, html):
		return BeautifulSoup(html,"lxml").find(id="articleContent").text

	def get_urls(self):
		maxId = 443029
		minId = 430001
		for newsID in range(maxId, minId, -1):
			if self.exists(newsID):
				continue
			else:
				url = "https://www.guokr.com/article/%s/" % newsID
				yield newsID, url