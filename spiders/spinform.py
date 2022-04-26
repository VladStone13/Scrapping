import scrapy
from scrapy.http import Request
from war2022_VMD.items import War2022VmdItem

class SpinformSpider(scrapy.Spider):
    name = 'spinform'
    allowed_domains = ['ru.spinform.ru']
    start_urls = ['http://ru.spinform.ru/']

    def start_requests(self):
        for link_url in self.start_urls:
            print(link_url)

            request = Request(link_url, cookies={'store_language': 'en'}, callback=self.parse)
            yield request

    def parse(self, response):
        item = War2022VmdItem()
        content = response.xpath('//div[@id="main_list"]/div')

        for article_link in content.xpath('.//a'):
            item['article_url'] = article_link.xpath('.//@href').extract_first()
            if item['article_url'].starswith("http"):
                continue
            item['article_url'] = "http://ru.spinform.ru//" + item['article_url']
            print(item['article_url'])
            yield (item)