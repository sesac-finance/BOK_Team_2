import scrapy

class CrawlingYonhab(scrapy.Spider):
    name = 'yonhab'

    def start_requests(self):
        urls = [
            "https://www.yna.co.kr/economy/"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        news_sels = response.css('ul#majorList.list > li')
        for news_sel in news_sels:
            title = news_sel.css('div > div.news-con > p::text').get()
            #desc = news_sel.css('a > ul > li > li::text').get()
            print('title:', title)
            #print('desc:', desc)s