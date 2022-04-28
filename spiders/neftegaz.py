import scrapy
from scrapy.http import Request
from war2022_VMD.items import War2022VmdItem

class NeftegazSpider(scrapy.Spider):
    name = 'neftegaz'
    allowed_domains = ['neftegaz.ru']
    start_urls = ['https://neftegaz.ru/news/', 'https://neftegaz.ru/news/2',
                  'https://neftegaz.ru/news/3', 'https://neftegaz.ru/news/4',
                  'https://neftegaz.ru/news/5', 'https://neftegaz.ru/news/6',
                  'https://neftegaz.ru/news/7', 'https://neftegaz.ru/news/8',
                  'https://neftegaz.ru/news/9', 'https://neftegaz.ru/news/10']

    def start_requests(self):
        for link_url in self.start_urls:
            print(link_url)

            request = Request(link_url, cookies={'store_language': 'en'}, callback=self.parse)
            yield request

    def parse(self, response):
        item = War2022VmdItem()

        content = response.xpath('//div[contains(@class, "news_week__item")]')

        isFirst = True
        for article_link in content.xpath('.//a'):
            if not isFirst:
                item['article_url'] = article_link.xpath('.//@href').extract_first()
                item['article_url'] = item['article_url']
                print(item['article_url'])
                yield (item)

            isFirst = not isFirst