import scrapy
from scrapy.http import Request
from war2022_VMD.items import War2022VmdItem
import json
import hashlib

class ComnewsArticlesSpider(scrapy.Spider):
    name = 'comnewsarticles'
    allowed_domains = ['comnews.ru']
    start_urls = []

    def start_requests(self):
        # Open the JSON file which contains article links
        data = []
        with open('./comnews.json') as json_file:
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
        item['article_title'] = response.xpath('//div[@class="s2"]').extract()
        item['article_text'] = "\n".join(response.xpath('//div[@class="field-items"]/div/p').extract())

        yield (item)
