import scrapy
from scrapy.http import Request
from war2022_VMD.items import War2022VmdItem
import json
import hashlib

class RbaArticlesSpider(scrapy.Spider):
    name = 'rbcarticles'
    allowed_domains = ['rbc.ru']
    start_urls = []

    def start_requests(self):
        # Open the JSON file which contains article links
        data = []
        with open('./rbc.json') as json_file:
            data = json.load(json_file)

        for link_url in data:
            print('URL: ' + link_url['article_url'])
            # Request to get the HTML content
            request = Request(link_url['article_url'],
                              cookies={'store_language': 'ru'},
                              callback=self.parse)
            yield request

    def parse(self, response):
        item = War2022VmdItem()
        item['article_link'] = response.url
        item['article_uuid'] = hashlib.sha256(str(response.url).encode('utf-8')).hexdigest()
        item['article_id'] = response.url.split("/")[-1]
        item['article_datetime'] = response.xpath('//span[@class="article__header__date"]').extract()
            # item['article_datetime_modified'] = response.xpath(
            #    '//div[@class="item-info"]/time[@itemprop="dateModified"]/@datetime').extract()
            # if not item['article_datetime_modified']:
            #    item['article_datetime_modified'] = response.xpath(
            #        '//div[@class="publication-info"]/time[@itemprop="dateModified"]/@datetime').extract()
        item['article_title'] = response.xpath('//h1[contains(@class,"article__header__title-in")]').extract()
        if not item['article_title']:
            item['article_title'] = response.xpath('//div[@class="publication"]/h1/text()').extract()

        item['article_text'] = "\n".join(response.xpath('//div[@class="article__text article__text_free"]/p').extract())
            # if not item['article_text']:
            #     item['article_text'] = "\n".join(response.xpath('//div[@class="item-text"]/div[3]//*/text()').extract())
        item['article_author'] = "\n".join(response.xpath('//span[@class="article__authors__author__name"]').extract())
        if not item['article_author']:
            item['article_author'] = "\n".join(response.xpath('//div[@itemprop="author"]/span/text()').extract())

        yield (item)
