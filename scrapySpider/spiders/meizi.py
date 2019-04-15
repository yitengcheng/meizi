# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapySpider.items import MeiziItem
from scrapy.loader import ItemLoader
from scrapySpider.utils.common import get_browser


class MeiziSpider(CrawlSpider):
    name = 'meizi'
    allowed_domains = ['www.mzitu.com']
    start_urls = ['https://www.mzitu.com/']
    cookie_dict = {}

    rules = (
        Rule(
            LinkExtractor(allow=r'\d+|\d+/\d+'),
            callback='parse_item',
            follow=True),
        Rule(LinkExtractor(allow=r'.+'), follow=True),
    )

    def parse_item(self, response):
        item_loader = ItemLoader(item=MeiziItem(), response=response)
        item_loader.add_css('img_url', '.main-image p a img::attr(src)')
        item_loader.add_css('title', '.main-title::text')
        item_loader.add_value('url', response.url)
        return item_loader.load_item()

    def parse_start_url(self, response):
        if not self.cookie_dict:
            brower = get_browser()
            brower.get('https://www.mzitu.com')
            cookies = brower.get_cookies()
            for cookie in cookies:
                self.cookie_dict[cookie['name']] = cookie['value']
        yield scrapy.Request(
            self.start_urls[0], dont_filter=True, cookies=self.cookie_dict)
