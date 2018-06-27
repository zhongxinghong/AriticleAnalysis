#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# fileame: zqbcyol.py
# 

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__),".."))

cachedir = os.path.join(os.path.dirname(__file__),"../cache/")
urlsFile = os.path.join(cachedir,"zqbcyol_urls.json")

from lib.util.utilfuncs import show_status, iter_split
from lib.spider import *
from lib.spider.error import *

import json
import re


__all__ = ["zqbcyolSpider"]


class zqbcyolSpider(Spider): # 中青报-冰点周刊

	def __init__(self):
		Spider.__init__(self)
		self.headers = {
			#"Host": "zqb.cyol.com",
			"Upgrade-Insecure-Requests": "1",
		}

		self.dbTable = "zqbcyol"
		self.workers = 32
		#self.Auto_Speed_Up = False
		self.Allow_Redirects = True #需要重定向
		self.Interval_Time = 0

		self.Response_Charset = ["utf-8","gbk","gb2312",None]


	def pre_get_urls(self):
		self.Use_Proxy = False
		self.Allow_Redirects = True
		self.headers = {
			#"Host": "zqb.cyol.com",
			"Upgrade-Insecure-Requests": "1",
		}

		try:
			urls = [
				"http://zqb.cyol.com/node/node_6443.htm",
				"http://zqb.cyol.com/node/node_3070.htm",
				"http://zqb.cyol.com/node/node_7046.htm",
				"http://zqb.cyol.com/node/node_3073.htm",
				"http://zqb.cyol.com/node/node_3072.htm",
				"http://zqb.cyol.com/node/node_3070.htm",
				"http://www.cyol.com/zqb/node_6443.htm",
				"http://www.cyol.com/zqb/node_6443_2.htm",
				"http://www.cyol.com/zqb/node_6443_3.htm",
				"http://www.cyol.com/zqb/node_6443_4.htm",
				"http://www.cyol.com/zqb/node_6443_5.htm",
			]

			newsUrl = []
			for url in urls:
				html = self.get(url)
				bodySoup = BeautifulSoup(html,"lxml")
				for ulSoup in bodySoup.find_all(class_="list_sty"):
					for a in ulSoup.find_all("a"):
						newsUrl.append(a.get("href",None))
				for a in bodySoup.find_all("a",class_="tit_width"):
					newsUrl.append(a.get("href",None))
		except NotFoundError as err:
			print(url)
			raise err
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

		reID1 = re.compile(r"content_(.*?).htm$")
		reID2 = re.compile(r"D110000zgqnb_(.*?).htm$")
		reNewsID1 = re.compile(r"^(\d{8})_(\d{1})-(\d{2})$")
		reNewsID2 = re.compile(r"^\d{7}$")
		for url in urls:
			#print(url)
			newsID = reID1.search(url) or reID2.search(url) or None
			if newsID:
				newsID = newsID.group(1)
				if reNewsID1.match(newsID):
					newsID = "".join(reNewsID1.match(newsID).group(1,2,3))
					newsID = int(newsID)
				elif reNewsID2.match(newsID):
					newsID = int(newsID)
					url = "http://zqb.cyol.com/" + url[3:]
				'''else:
					print(newsID) # None !'''
				if not self.exists(newsID):
					yield newsID, url

	def parse_html(self, html):
		bodySoup = BeautifulSoup(html,"lxml")
		if bodySoup.find(id="ozoom"):
			return " ".join([p.text for p in bodySoup.find(id="ozoom").find_all("p")]) 
		elif bodySoup.find(id="content-main"):
			return bodySoup.find(id="content-main").find_all("div")[-1].text


if __name__ == '__main__':
	spider = zqbcyolSpider()
	#spider.pre_get_urls()
	spider.work(loop=True, errs=["ServerError","NotFound","EmptyPage","Null","DecodeError"])
