# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     GetFreeProxy.py
   Description :  抓取免费代理
   Author :       JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25:
-------------------------------------------------
"""
import re
import sys
import requests


try:
    from importlib import reload  # py3 实际不会实用，只是为了不显示语法错误
except:
    reload(sys)
    sys.setdefaultencoding('utf-8')

sys.path.append('..')

from Util.utilFunction import robustCrawl, getHtmlTree
from Util.WebRequest import WebRequest
from Util.utilFunction import verifyProxyFormat

# for debug to disable insecureWarning
requests.packages.urllib3.disable_warnings()

"""
    66ip.cn
    data5u.com
    xicidaili.com
    goubanjia.com
    xdaili.cn
    kuaidaili.com
    cn-proxy.com
    proxy-list.org
    www.mimiip.com to do
"""


class GetFreeProxy(object):
    """
    proxy getter
    """

    def __init__(self):
        pass

    @staticmethod
    def freeProxyFirst(page=10):
        """
        无忧代理 http://www.data5u.com/
        几乎没有能用的
        :param page: 页数
        :return:
        """
        url_list = [
            'http://www.data5u.com/',
            'http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gnpt/index.shtml'
        ]
        for url in url_list:
            html_tree = getHtmlTree(url)
            ul_list = html_tree.xpath('//ul[@class="l2"]')
            for ul in ul_list:
                try:
                    yield ':'.join(ul.xpath('.//li/text()')[0:2])
                except Exception as e:
                    print(e)

    @staticmethod
    def freeProxySecond(area=33, page=1):
        """
        代理66 http://www.66ip.cn/
        :param area: 抓取代理页数，page=1北京代理页，page=2上海代理页......
        :param page: 翻页
        :return:
        """
        area = 33 if area > 33 else area
        for area_index in range(1, area + 1):
            for i in range(1, page + 1):
                url = "http://www.66ip.cn/areaindex_{}/{}.html".format(area_index, i)
                html_tree = getHtmlTree(url)
                tr_list = html_tree.xpath("//*[@id='footer']/div/table/tr[position()>1]")
                if len(tr_list) == 0:
                    continue
                for tr in tr_list:
                    yield tr.xpath("./td[1]/text()")[0] + ":" + tr.xpath("./td[2]/text()")[0]
                break

    @staticmethod
    def freeProxyThird(days=1):
        """
        ip181 http://www.ip181.com/  不能用了
        :param days:
        :return:
        """
        url = 'http://www.ip181.com/'
        html_tree = getHtmlTree(url)
        try:
            tr_list = html_tree.xpath('//tr')[1:]
            for tr in tr_list:
                yield ':'.join(tr.xpath('./td/text()')[0:2])
        except Exception as e:
            pass

    @staticmethod
    def freeProxyFourth(page=2):
        """
        西刺代理 http://www.xicidaili.com
        :return:
        """
        url_list = [
            'http://www.xicidaili.com/nn/',  # 高匿
            'http://www.xicidaili.com/nt/',  # 透明
        ]
        for each_url in url_list:
            for i in range(1, page + 1):
                page_url = each_url + str(i)
                tree = getHtmlTree(page_url)
                proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in proxy_list:
                    try:
                        yield ':'.join(proxy.xpath('./td/text()')[0:2])
                    except Exception as e:
                        pass

    @staticmethod
    def freeProxyFifth():
        """
        guobanjia http://www.goubanjia.com/
        :return:
        """
        url = "http://www.goubanjia.com/"
        tree = getHtmlTree(url)
        proxy_list = tree.xpath('//td[@class="ip"]')
        # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
        # 需要过滤掉<p style="display:none;">的内容
        xpath_str = """.//*[not(contains(@style, 'display: none'))
                                        and not(contains(@style, 'display:none'))
                                        and not(contains(@class, 'port'))
                                        ]/text()
                                """
        for each_proxy in proxy_list:
            try:
                # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
                ip_addr = ''.join(each_proxy.xpath(xpath_str))
                port = each_proxy.xpath(".//span[contains(@class, 'port')]/text()")[0]
                yield '{}:{}'.format(ip_addr, port)
            except Exception as e:
                pass

    @staticmethod
    def freeProxySixth():
        """
        讯代理 http://www.xdaili.cn/
        :return:
        """
        url = 'http://www.xdaili.cn/ipagent/freeip/getFreeIps?page=1&rows=10'
        request = WebRequest()
        try:
            res = request.get(url).json()
            for row in res['RESULT']['rows']:
                yield '{}:{}'.format(row['ip'], row['port'])
        except Exception as e:
            pass

    @staticmethod
    def freeProxySeventh():
        """
        快代理 https://www.kuaidaili.com
        """
        url_list = [
            'https://www.kuaidaili.com/free/inha/{page}/',
            'https://www.kuaidaili.com/free/intr/{page}/'
        ]
        for url in url_list:
            for page in range(1, 5):
                page_url = url.format(page=page)
                tree = getHtmlTree(page_url)
                proxy_list = tree.xpath('.//table//tr')
                for tr in proxy_list[1:]:
                    yield ':'.join(tr.xpath('./td/text()')[0:2])

    @staticmethod
    def freeProxyEight(page=10):
        """
        秘密代理 http://www.mimiip.com
        """
        url_gngao = ['http://www.mimiip.com/gngao/%s' % n for n in range(1, page+1)]  # 国内高匿
        url_gnpu = ['http://www.mimiip.com/gnpu/%s' % n for n in range(1, page+1)]  # 国内普匿
        url_gntou = ['http://www.mimiip.com/gntou/%s' % n for n in range(1, page+1)]  # 国内透明
        url_list = url_gngao + url_gnpu + url_gntou

        request = WebRequest()
        for url in url_list:
            r = request.get(url, use_proxy=True)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W].*<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)

    @staticmethod
    def freeProxyNinth(page=10):
        """
        码农代理 https://proxy.coderbusy.com/
        :return:
        """
        urls = ['https://proxy.coderbusy.com/classical/country/cn.aspx?page=%s' % n for n in range(1, page+1)]
        request = WebRequest()
        for url in urls:
            r = request.get(url)
            proxies = re.findall('data-ip="(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})".+?>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)

    @staticmethod
    def freeProxyTen():
        """
        云代理 http://www.ip3366.net/free/
        :return:
        """
        urls = ['http://www.ip3366.net/free/']
        request = WebRequest()
        for url in urls:
            r = request.get(url)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxyEleven():
        """
        IP海 http://www.iphai.com/free/ng
        :return:
        """
        urls = [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/wp'
        ]
        request = WebRequest()
        for url in urls:
            r = request.get(url)
            proxies = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
                                 r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxyTwelve(page=6):
        """
        guobanjia http://ip.jiangxianli.com/?page=
        免费代理库
        超多量
        :return:
        """
        for i in range(1, page+1):
            url = 'http://ip.jiangxianli.com/?page={}'.format(i)
            # print(url)
            html_tree = getHtmlTree(url)
            tr_list = html_tree.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr")
            if len(tr_list) == 0:
                continue
            for tr in tr_list:
                yield tr.xpath("./td[2]/text()")[0] + ":" + tr.xpath("./td[3]/text()")[0]

    @staticmethod
    def freeProxyWallFirst():
        """
        墙外网站 cn-proxy
        :return:
        """
        urls = ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
        request = WebRequest()
        for url in urls:
            r = request.get(url)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)

    @staticmethod
    def freeProxyWallSecond(page=10):
        """
        https://proxy-list.org/english/index.php
        :return:
        """
        urls = ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, page+1)]
        request = WebRequest()
        import base64
        for url in urls:
            r = request.get(url)
            proxies = re.findall(r"Proxy\('(.*?)'\)", r.text)
            for proxy in proxies:
                yield base64.b64decode(proxy).decode()

    @staticmethod
    def freeProxyWallThird():
        urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1']
        request = WebRequest()
        for url in urls:
            r = request.get(url)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)


if __name__ == '__main__':
    gg = GetFreeProxy()

    # test_batch(gg.freeProxyFirst())

    # test_batch(gg.freeProxySecond())

    # test_batch(gg.freeProxyFourth())

    # test_batch(gg.freeProxyFifth())

    # test_batch(gg.freeProxySixth())

    # test_batch(gg.freeProxySeventh())

    # test_batch(gg.freeProxyEight())

    # test_batch(gg.freeProxyNinth())

    # test_batch(gg.freeProxyTen())

    # test_batch(gg.freeProxyEleven())

    proxy_iter = gg.freeProxyTwelve()
    proxy_set = set()
    for proxy in proxy_iter:
        proxy = proxy.strip()
        if proxy and verifyProxyFormat(proxy):
            #self.log.info('{func}: fetch proxy {proxy}'.format(func=proxyGetter, proxy=proxy))
            proxy_set.add(proxy)
        #else:
            #self.log.error('{func}: fetch proxy {proxy} error'.format(func=proxyGetter, proxy=proxy))

        # store
    for proxy in proxy_set:
        print(proxy)


    # test_batch(gg.freeProxyTwelve())

    # test_batch(gg.freeProxyWallFirst())

    # test_batch(gg.freeProxyWallSecond())

    # test_batch(gg.freeProxyWallThird())
