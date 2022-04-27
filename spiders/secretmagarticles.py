import scrapy
from scrapy.http import Request
from war2022_VMD.items import War2022VmdItem
import json
import hashlib

class SecretmagArticlesSpider(scrapy.Spider):
    name = 'secretmagarticles'
    allowed_domains = ['rbc.ru']
    start_urls = []

    def start_requests(self):
        # Open the JSON file which contains article links
        data = []
        with open('./secretmag.json') as json_file:
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
        item['article_uuid'] = hashlib.sha256(str(response.url).encode('utf-8')).hexdigest()
        item['article_title'] = response.xpath('//h1').extract()
        if not item['article_title']:
            item['article_title'] = response.xpath('//div[@class="publication"]/h1/text()').extract()

        item['article_text'] = "\n".join(response.xpath('//div[contains(@class,"lead")]/p').extract()) + "\n".join(response.xpath('//div[contains(@class,"text")]/p').extract())

        yield (item)
