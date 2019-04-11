# coding:utf-8

from scrapy.spiders import CrawlSpider, Request, Rule
from rottentomatoes.items import RottentomatoesItem
from scrapy.linkextractors import LinkExtractor


class RottentomatoesSpider(CrawlSpider):
    name = 'rottentomatoes'
    allowed_domains = ['www.rottentomatoes.com']
    rules = (
        Rule(LinkExtractor(allow=r"/m/[^/]+$"), callback="parse_rottentomatoes", follow=True),
    )

    def start_requests(self):
        pages = []
        for i in range(1900,1960):
            url = "https://www.rottentomatoes.com/top/bestofrt/?year=" + str(i)
            yield Request(url=url, callback=self.parse)

    def parse_rottentomatoes(self, response):
        item = RottentomatoesItem()
        item['url'] = response.url
        item['title'] = "".join(response.xpath('//*[@id="topSection"]/div[2]/div[1]/h1/text()').extract())
        item['rating'] = "".join("".join(response.xpath('//*[@id="tomato_meter_link"]/span[2]/text()').extract()).split())
        s = 1
        while "".join(response.xpath('//*[@id="mainColumn"]/section['+str(s)+']/div/h2/text()').extract())!="Movie Info" :
            s+=1
        item['genre'] = " ".join("".join(response.xpath('//*[@id="mainColumn"]/section['+str(s)+']/div/div/ul/li[2]/div[2]/a/text()').extract()).split())
        item['level'] = "".join(response.xpath('//*[@id="mainColumn"]/section['+str(s)+']/div/div/ul/li[1]/div[2]/text()').extract())
        item['director'] = "".join(response.xpath('//*[@id="mainColumn"]/section['+str(s)+']/div/div/ul/li[3]/div[2]/a/text()').extract())
        item['writer'] = "".join(response.xpath('//*[@id="mainColumn"]/section['+str(s)+']/div/div/ul/li[4]/div[2]/a/text()').extract())

        pos = 4
        if '\n' not in "".join(response.xpath('//*[@id="mainColumn"]/section['+str(s)+']/div/div/ul/li[5]/div[2]/time/text()').extract()):
            pos += 1
        item['time'] = "".join(response.xpath('//*[@id="mainColumn"]/section['+str(s)+']/div/div/ul/li['+str(pos)+']/div[2]/time/text()').extract())
        pos += 1
        if ',' in "".join("".join(response.xpath('//*[@id="mainColumn"]/section['+str(s)+']/div/div/ul/li['+str(pos)+']/div[2]/time/text()').extract()).split()):
            pos += 1
        if '$' in "".join(response.xpath('//*[@id="mainColumn"]/section['+str(s)+']/div/div/ul/li['+str(pos)+']/div[2]/text()').extract()):
            pos += 1
        item['runtime'] = " ".join("".join(response.xpath('//*[@id="mainColumn"]/section['+str(s)+']/div/div/ul/li['+str(pos)+']/div[2]/time/text()').extract()).split())
        item['studio'] = "".join(response.xpath('//*[@id="mainColumn"]/section['+str(s)+']/div/div/ul/li['+str(pos+1)+']/div[2]/a/text()').extract())
        if item['studio'] == "": item['studio'] = " ".join("".join(response.xpath('//*[@id="mainColumn"]/section['+str(s)+']/div/div/ul/li['+str(pos+1)+']/div[2]/text()').extract()).split())
        yield item
