import scrapy
from scrapy.http import Request
from war2022_VMD.items import War2022VmdItem


class SecretmagSpider(scrapy.Spider):
    name = 'secretmag'
    allowed_domains = ['secretmag.ru']
    start_urls = ['http://secretmag.ru/', 'https://secretmag.ru/news?page=2', 'https://secretmag.ru/news?page=3',
                  'https://secretmag.ru/news?page=4', 'https://secretmag.ru/news?page=5', 'https://secretmag.ru/news?page=6',
                  'https://secretmag.ru/news?page=7', 'https://secretmag.ru/news?page=8', 'https://secretmag.ru/news?page=9',
                  'https://secretmag.ru/news?page=10', 'https://secretmag.ru/news?page=11', 'https://secretmag.ru/news?page=12']

    def start_requests(self):
        for link_url in self.start_urls:
            print(link_url)

            request = Request(link_url, cookies={'store_language': 'en'}, callback=self.parse)
            yield request

    def parse(self, response):
        item = War2022VmdItem()

        content = response.xpath('//div[contains(@class, "jsx-2155360971 _39FNd9SD _2tnX_KS0 jsx-1008381604 item _22ATwFqf")]')
        if not content:
            content = response.xpath('//div[contains(@class, "jsx-2155360971 _39FNd9SD _2tnX_KS0  jsx-1008381604 item _22ATwFqf")]')

        for article_link in content.xpath('.//a'):
            item['article_url'] = article_link.xpath('.//@href').extract_first()
            item['article_url'] = 'https://secretmag.ru' + item['article_url']
            print(item['article_url'])
            yield (item)
