当前目录存放的代码为使用scrapy爬取动态页面的示例

1.air_history为scrapy结合selenium爬取天气的一个示例
获取各个城市近年来每天的空气质量
	日期
	城市
	空气质量指数
	空气质量等级
	pm2.5
	pm10
	so2
	co
	no2
	o3

使用scrapy
scrapy操作的基本流程如下：
1.创建项目：scrapy startproject 项目名称
2.新建爬虫：scrapy genspider 爬虫文件名 爬虫基础域名
3.编写item
4.spider最后return item
5.在setting中修改pipeline配置
6.在对应pipeline中进行数据持久化操作
创建
打开命令行，输入scrapy startproject air_history ,创建一个名为air_history的scrapy项目

进入该文件夹，输入scrapy genspider area_spider "aqistudy.cn",可以发现在spiders文件夹下多了一个名为area_spider的py文件