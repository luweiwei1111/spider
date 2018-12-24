# -*- coding: utf-8 -*-

class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

if __name__ == "__main__":
    cookie = "JSESSIONID=5DA43BB8C9A8774C18C507DBD695DBBA; __jsluid=c223b00964f5765206cef21adef5e02f; bdshare_firstime=1544702564332"
    trans = transCookie(cookie)
    print(trans.stringToDict())