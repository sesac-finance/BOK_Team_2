# -*- coding: utf-8 -*-

import scrapy
import datetime

class CrawlingScrapy(scrapy.Spider):
    name = 'EdailyCrawler'
    
    
    def start_requests(self):
        date = datetime.date(2010, 1, 1)

        while date <= datetime.date(2022, 11, 20):
            date1 = '.'.join(str(date).split('-'))
            #print('.'.join(str(date1).split('-')))
            date2= date + datetime.timedelta(days=1)
            date3 = '.'.join(str(date2).split('-'))
            date += datetime.timedelta(days=1)
            news_site = []
            urls = 'https://search.naver.com/search.naver?where=news&query=%EA%B8%88%EB%A6%AC&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds={}&de={}&docid=&related=0&mynews=1&office_type=2&office_section_code=8&news_office_checked=1018&nso=so%3Ar%2Cp%3Afrom20221120to20221121&is_sug_officeid=0'.format(date1, date3)
            print(urls)
            headers = {"user-agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

            # for url in urls:
            yield scrapy.Request(url=urls, headers = headers, callback=self.link_parse)

    def link_parse(self, response):
        news_sels = response.css('ul.list_news > li')
        for news_sel in news_sels:
            for href in news_sel.css('div.news_area > a[href]::attr(href)'):
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item={}
        dirs = response.css('div.news_body::text').extract()
        strp = []
        for dir in dirs:
            strp.append(dir.strip()) 
        
        item['news_date'] = response.css('#contents > section.center1080.position_r > section.aside_left > div.article_news > div.news_titles > div > div > ul > li:nth-child(1) > p:nth-child(1)::text').get()
        item['news_dir'] = strp
        # for text in response.css('div.news_body::text').extract():
        #     print('total:', text)
        #print('len:', len(response.css('div.news_body::text')))
        # for sel in sels:
        #     dir = sel.css('p::text').get() 
        print(item)
        return item



