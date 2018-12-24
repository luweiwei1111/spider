# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.selector import Selector
from bs4 import BeautifulSoup
import re
import urllib

class CnvdLoginSpider(scrapy.Spider):
    name = 'cnvd_login'
    allowed_domains = ['www.cnvd.org.cn']  # 允许爬取的域名，非此域名的网页不会爬取
    start_urls = [
        # 起始url，这里设置为从最大tid开始，向0的方向迭代
        "http://www.cnvd.org.cn/shareData/list"
    ]

    base_url = 'http://www.cnvd.org.cn'

    # 用来保持登录状态，可把chrome上拷贝下来的字符串形式cookie转化成字典形式，粘贴到此处
    cookies = {'bdshare_firstime': '1544702564332', '__jsluid': 'c223b00964f5765206cef21adef5e02f', 'JSESSIONID': '5DA43BB8C9A8774C18C507DBD695DBBA'}

    # 发送给服务器的http头信息，有的网站需要伪装出浏览器头进行爬取，有的则不需要
    headers = {
        # 'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }

    def start_requests(self):
        """
        这是一个重载函数，它的作用是发出第一个Request请求
        :return:
        """
        # 带着headers、cookies去请求self.start_urls[0],返回的response会被送到
        # 回调函数parse中
        yield Request(self.start_urls[0],
                             callback=self.cnvd_logins, headers=self.headers,
                             cookies=self.cookies, meta=self.meta)

    def cnvd_logins(self, response):
        selector = Selector(response)  # 创建选择器
        page_num = selector.xpath('//*[@id="patchList"]/div/span[3]/@data').extract_first()  # 取出所有页数
        print(page_num)
        # for item in page_num:
        # 	print(item['data'])
        soup = BeautifulSoup(response.text, 'lxml')

        href_list = soup.find_all('a', href=re.compile("/shareData/download/"))
        for item in href_list:
        	print(item['href'])
        	download_url = self.base_url + item['href']
        	print('download_url:' + download_url)
        	download_url = 'http://nsclick.baidu.com/v.gif?pid=307&type=3075&l=1065981&t=295&s=867492&v=150&f=33000&r=http%3A%2F%2Fwww.cnvd.org.cn%2FshareData%2Flist%3Fmax%3D10%26offset%3D10&u=http%3A%2F%2Fwww.cnvd.org.cn%2FshareData%2Flist%3Fmax%3D10%26offset%3D20'
        	urllib.request.urlretrieve(download_url, './xml')
    #     yield Request(url, self.get_cnvd_detail)

    # def get_cnvd_detail(self, response):
    	#<a href="/shareData/download/505" title="下载xml">2018-12-03_2018-12-09.xml</a>
        
