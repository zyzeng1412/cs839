# coding:utf-8
#!/usr/bin/python 

from scrapy import cmdline

cmdline.execute("scrapy crawl imdb -o imdb.csv".split())
