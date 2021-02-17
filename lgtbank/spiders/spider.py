import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from ..items import LgtbankItem



class SpiderSpider(scrapy.Spider):
    name = 'spider'

    start_urls = ['https://www.lgt.at/en/news/']


    def parse(self,response):
        links = response.xpath('//div[@class="col-sm-12"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(LgtbankItem())
        item.default_output_processor = TakeFirst()
        date = response.xpath('//div[@class="time-stamp"]//text()').get()
        title = response.xpath('//h1//text()').get()
        content = response.xpath('//div[@class="col-xs-12    "]/*[not (self::script)]//text()').getall()
        content = ' '. join([text.strip() for text in content if text.strip()][3:-1])

        item.add_value('date', date)
        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)
        return item.load_item()
