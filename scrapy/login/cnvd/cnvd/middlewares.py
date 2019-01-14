from scrapy import signals
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class CnvdDownloaderMiddleware(object):
    def process_request(self, request, spider):
        print('#########middleware url:', request.url)
        #if '/shareData/download/' in request.url:
        #    return
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        
        # 指定谷歌浏览器路径
        # <a href="/shareData/download/489" title="下载xml">2018-10-08_2018-10-14.xml</a>
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/usr/bin/chromedriver')

        print('shareData url:', request.url)
        self.driver.get(request.url)
        time.sleep(2)
        print(self.driver.title)
        html = self.driver.page_source
        self.driver.quit()
        return scrapy.http.HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8',
                                        request=request)