import scrapy

class CrawlingScrapy(scrapy.Spider):
    name = 'crawler'

    def start_requests(self):
        urls = [
            'https://www.edaily.co.kr/search/index?keyword=%EA%B8%88%EB%A6%AC'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        news_sels = response.css('div#newsList > div')
        for news_sel in news_sels:
            hrefs = news_sel.css('a[href]::attr(href)').get()
            href_list= []
            for href in hrefs:
                append(href)
                yield scrapy.Request('https://www.edaily.co.kr/{}'.format(href), callback=self.parse)
            # #response.css('a[href*=image]::attr(href)').extract()
            # # driver = news_sel.request.meta['driver']
            # # button = driver.get_element_by_css('a > ul')
            # # button.click()	
            # # news_title = response.css('div.news_titles > h2::text').get
            # print(desc)

    # def parses(self, response):
    #     news = response.css('div.news_body::text').get()
    #     print(news)
