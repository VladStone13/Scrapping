import scrapy
from scrapy.http import Request
from war2022_VMD.items import War2022VmdItem

class ComnewsSpider(scrapy.Spider):
    name = 'comnews'
    allowed_domains = ['comnews.ru']
    start_urls = ['https://comnews.ru/sanctions2022', 'https://www.comnews.ru/sanctions2022?page=1',
                  'https://www.comnews.ru/sanctions2022?page=2', 'https://www.comnews.ru/sanctions2022?page=3']

    def start_requests(self):
        for link_url in self.start_urls:
            print(link_url)

            request = Request(link_url, cookies={'store_language': 'en'}, callback=self.parse)
            yield request

    def parse(self, response):
        item = War2022VmdItem()

        content = response.xpath('//div[contains(@class, "node no-img")]')
        prev_url = ""

        for article_link in content.xpath('.//a'):
            url = article_link.xpath('.//@href').extract_first()
            if url == prev_url:
                item['article_url'] = "https://comnews.ru" + url
                print(item['article_url'])
                yield (item)

            prev_url = url
