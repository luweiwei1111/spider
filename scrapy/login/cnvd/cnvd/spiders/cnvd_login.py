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
    file_name_hd = 'cnvd_xml_'
    cnt = 0
    head_url = 'http://www.cnvd.org.cn/shareData/list?max=10&offset='

    # 用来保持登录状态，可把chrome上拷贝下来的字符串形式cookie转化成字典形式，粘贴到此处
    cookies = {'__jsluid': 'cfb4c27eac28206e7a066f61eecca3c6', 'bdshare_firstime': '1538076489584', 'JSESSIONID': '0DE9FF4B0BF25EAF0D0A20366E36BCE3'}
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
        # selector = Selector(response)  # 创建选择器
        # page_num = selector.xpath('//*[@id="patchList"]/div/span[3]/@data').extract_first()  # 取出所有页数
        # print(page_num)
        
        #http://www.cnvd.org.cn/shareData/list?max=10&offset=0
        page_num = 22
        for i in range(0, int(page_num)):
            url = self.head_url + str(i*10)
            yield Request(url, callback=self.find_url, headers=self.headers, cookies=self.cookies, meta=self.meta)

    def find_url(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        href_list = soup.find_all('a', href=re.compile("/shareData/download/"), title="下载xml")
        count = 0
        for item in href_list:
            #print(item['href'])
            file = item.text
            url = self.base_url + item['href']
            print('#####file:%s, url:%s'%(file, url))
            yield Request(url, callback=self.download_file, headers=self.headers, cookies=self.cookies, meta=self.meta)

    def download_file(self, response):
        self.cnt = self.cnt + 1
        file_name = './xml/' + self.file_name_hd + str(self.cnt) + '.xml'
        #print('file_name:', file_name)
        #print('file_name:', self.file_name)
        try:
            with open(file_name, 'w') as f:
                f.write(response.text)
                print('####write file %s OK'%(file_name))
        except:
            print('##ERROR# write file %s failed'%(file_name))