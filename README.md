## 应用商城抓取版本号
**注意：这个脚本只是抓取排在第一app的版本号，有时排在第一的app，并不是想要的。所以需要去核实每一个 first_search_result 是不是你要找的。**

5大商城：

中国移动应用商场

360手机助手

应用宝官网

豌豆荚

百度手机助手 


## 安装
1、Python 2.7

2、Scrapy：http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/install.html

3、安装 Selenium+Phantomjs : 因为抓取 QQ 应用宝是用 JS 动态生成页面，所以要用 Scrapy+Selenium+Phantomjs http://jiayi.space/post/scrapy-phantomjs-seleniumdong-tai-pa-chong

4、下载安装后，在 app-version-spiders/appbot/middlewares.py 修改 PhantomJS 中 phantomjs.exe 的路径。如："driver = webdriver.PhantomJS(executable_path=r'E:\software\phantomjs\phantomjs-2.1.1-windows\bin\phantomjs.exe')" 

## 使用
1、将整个项目 git clone(已经安装了 git)或是 Download、解压

2、在 /appbot/input/appName.txt 文件中，输入 app name

3、在 目录/appbot 中打开命令行窗口，输入命令行 scrapy crawl + 爬虫 + -o + 输出路径，为 xml 格式 

**(运行前首先要删除 /appbot/output 文件夹中的文件或是修改输出路径，否则运行第 2 次，而输出的路径相同，它会追加，这样会导致 xml 文件失败。)：**

scrapy crawl 360zhushou -o ./output/360zhushou.xml

scrapy crawl baidushouji -o ./output/baidushouji.xml

scrapy crawl mm -o ./output/mm.xml

scrapy crawl wandoujia -o ./output/wandoujia.xml

scrapy crawl qq -o ./output/qq.xml

**假如运行第 2次，而输出的路径相同，它会追加，这样会导致 xml 文件失败。**

4、打开 xml 格式：打开任意一个 Excel 文件，将 /appbot/output/360zhushou.xml 移到文件，自动打开；

* 下图为在360助手抓取的版本号


![在360助手抓取的版本号](https://github.com/sunshineliang/app-version-spiders/raw/master/picture/version.png)


key_word：为 /appbot/input/appName.txt 的 app name

search_word: 是把 key_word 经过处理(如：去掉后面括号……)

first_search_result：排在第一个搜索结果(假如为“需重新抓取”或是“找不到”，最好手动去找了)

version：第一个搜索结果的版本号(假如为“需重新抓取”或是“找不到”，最好手动去找了)

**注意：这个脚本只是抓取排在第一app的版本号，有时排在第一的app，并不一定是想要找的。所以需要去核实每一个 first_search_result 。**

比如：

key_word：腾讯自选股

search_word：腾讯自选股

first_search_result：自选股

version：5.6.0

在360助手搜索：腾讯自选股，而排在第一的是 ：自选股，这时候要确认这是不是要找的那个 app，有时候 first_search_result 与 search_word 相同，也并不代表是要找的。

## TODO：
* 重构代码;
