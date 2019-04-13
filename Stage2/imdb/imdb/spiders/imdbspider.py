# coding:utf-8

from scrapy.spiders import CrawlSpider, Request, Rule
from imdb.items import ImdbItem
from scrapy.linkextractors import LinkExtractor


class ImdbSpider(CrawlSpider):
    name = 'imdb'
    allowed_domains = ['www.imdb.com']
    rules = (
        Rule(LinkExtractor(allow=r"/title/tt\d+$"), callback="parse_imdb", follow=True),
    )

    def start_requests(self):
        #for i in range(1, 5):
        url = "https://www.imdb.com/search/title?title_type=feature&release_date=2018-01-01,2019-05-01"
        yield Request(url=url, callback=self.parse)

    def parse_imdb(self, response):
        item = ImdbItem()
        try:
            item['video_url'] = response.url
            item['video_title'] = "".join(response.xpath('//*[@class="title_wrapper"]/h1/text()').extract())
            item['video_year'] = "".join(response.xpath('//*[@id="titleYear"]/a/text()').extract())

            item['video_level'] = "".join(response.xpath('//*[@class="subtext"]/text()').extract())
            item['video_genres'] = "".join(response.xpath('//*[@class="subtext"]/a/text()').extract())
            yield item
        except Exception as error:
            log(error)
