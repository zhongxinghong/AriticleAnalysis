#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# fileame: main.py


from spiders import *


if __name__ == '__main__':
	#spider = jiemianSpider()
	#spider = nfpeopleSpider()
	#spider = infzmSpider()
	#spider = thepaperSpider()
	#spider = guokrSpider()
	#spider = qdailySpider()
	spider = zqbcyolSpider()
	
	spider.trail()
	#spider.work(loop=True,errs=["ServerError","Null","NotFound","EmptyPage"])
	
	#spider.trial(50875)

	#spider.work(loop=False,errs=["NotFound","EmptyPage"])
