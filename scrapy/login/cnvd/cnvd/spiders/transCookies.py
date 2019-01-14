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
    #Cookie: __jsluid=cfb4c27eac28206e7a066f61eecca3c6; bdshare_firstime=1538076489584; JSESSIONID=0DE9FF4B0BF25EAF0D0A20366E36BCE3

    cookie = "__jsluid=cfb4c27eac28206e7a066f61eecca3c6; bdshare_firstime=1538076489584; JSESSIONID=0DE9FF4B0BF25EAF0D0A20366E36BCE3"
    trans = transCookie(cookie)
    print(trans.stringToDict())