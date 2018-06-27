#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# fileame: /spiders/__init__.py
# 

from .guokr import guokrSpider
from .infzm import infzmSpider
from .jiemian import jiemianSpider
from .nfpeople import nfpeopleSpider
from .qdaily import qdailySpider
from .thepaper import thepaperSpider
from .zqbcyol import zqbcyolSpider
from .dailyzhihu import dailyzhihuSpider
from .lifeweek import lifeweekSpider
from .idaxiang import idaxiangSpider


__all__ = [
	"guokrSpider",		# 果壳
	"infzmSpider",		# 南方周末
	"jiemianSpider",	# 界面
	"nfpeopleSpider",	# 南方人物
	"qdailySpider", 	# 好奇心杂志
	"thepaperSpider", 	# 澎湃
	"zqbcyolSpider", 	# 中青报-冰点周刊
	"dailyzhihu", 		# 知乎日报
	"lifeweek",			# 三联生活周刊
	"idaxiang", 		# 大象公会-凤凰网
]