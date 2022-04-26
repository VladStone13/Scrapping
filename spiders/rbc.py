import scrapy
from scrapy.http import Request
from war2022_VMD.items import War2022VmdItem

class RbcSpider(scrapy.Spider):
    name = 'rbc'
    allowed_domains = ['www.rbc.ru']
    start_urls = ['https://www.rbc.ru/tags/?tag=%D0%AD%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0']

    def start_requests(self):
        for link_url in self.start_urls:
            print(link_url)

            request = Request(link_url, cookies={'store_language': 'en'}, callback=self.parse)
            yield request

    def parse(self, response):
        item = War2022VmdItem()

        content = response.xpath('//div[contains(@class, "search-item__wrap")]')

        for article_link in content.xpath('.//a'):
            item['article_url'] = article_link.xpath('.//@href').extract_first()
            item['article_url'] = item['article_url']
            print(item['article_url'])
            yield (item)