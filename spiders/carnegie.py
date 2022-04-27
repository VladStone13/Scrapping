import scrapy
from scrapy.http import Request
from war2022_VMD.items import War2022VmdItem


class CarnegieSpider(scrapy.Spider):
    name = 'carnegie'
    allowed_domains = ['carnegie.ru']
    start_urls = ['https://carnegie.ru/programs/all/742?lang=ru&pageOn=1', 'https://carnegie.ru/programs/all/742?lang=ru&pageOn=2',
                  'https://carnegie.ru/programs/all/742?lang=ru&pageOn=3', 'https://carnegie.ru/programs/all/742?lang=ru&pageOn=4',
                  'https://carnegie.ru/programs/all/742?lang=ru&pageOn=5', 'https://carnegie.ru/programs/all/742?lang=ru&pageOn=6',
                  'https://carnegie.ru/programs/all/742?lang=ru&pageOn=7', 'https://carnegie.ru/programs/all/742?lang=ru&pageOn=8',
                  'https://carnegie.ru/programs/all/742?lang=ru&pageOn=9', 'https://carnegie.ru/programs/all/742?lang=ru&pageOn=10']

    def start_requests(self):
        for link_url in self.start_urls:
            print(link_url)

            request = Request(link_url, cookies={'store_language': 'en'}, callback=self.parse)
            yield request

    def parse(self, response):
        item = War2022VmdItem()

        content = response.xpath('//li[contains(@class, "clearfix ")]')

        for article_link in content.xpath('.//a'):
            url = item['article_url'] = article_link.xpath('.//@href').extract_first()
            if url.find("ru-pub") != -1:
                item['article_url'] = url
                print(item['article_url'])
                yield (item)