#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# fileame: qdaily.py
# 

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__),".."))
from lib.spider import *

__all__ = ["qdailySpider"]


class qdailySpider(Spider): # 好奇心日报

	def __init__(self):
		Spider.__init__(self)
		self.headers = {
			"Host": "www.qdaily.com",
			"Origin": "http://www.qdaily.com/",
			"Cookie": "_qdaily4_web_session=b2svOHFFamtqd01tUGJhby9rS085MUdjY29CK1E0VFVOaEtwdEo1ajhRWGVySWk2YzVhdGdrYmNmVnBBQjRKWm42alAvN0NybE5PWVVxSlRKSzR1dzY5T0lTQW1nRy8zb1ZJQjhnV2tFK1NOckw2RFhQY0dpNTc3RDFBOC91elpzbncxcjZhaGZTQUduQWw5NjNJT25nPT0tLWRUaDc4VldSbm4wYUhOZWJxZ1p2dVE9PQ%3D%3D--7229dbb1ced5d24521d1ffe391d491214c0aed9d; _ga=GA1.2.325603013.1529653022; _gid=GA1.2.1439612500.1529653022",
			"Upgrade-Insecure-Requests": "1",
			"Connection": "keep-alive",
			"Referer": "http://www.qdaily.com/",
			#"If-None-Match": 'W/"5b2ca462-a7a0"',
		}

		self.dbTable = "qdaily"
		self.workers = 8
		self.Auto_Speed_Up = False
		self.Allow_Redirects = True # 需要重定向
		self.Response_Charset = "utf-8"

	def parse_html(self, html):
		return BeautifulSoup(html,"lxml").find(["p","div"],"detail").text

	def get_urls(self):
		maxId = 54534
		for newsID in range(maxId, 0, -1):
			if self.exists(newsID):
				continue
			else:
				url = "http://www.qdaily.com/articles/%s.html" % newsID
				yield newsID, url

