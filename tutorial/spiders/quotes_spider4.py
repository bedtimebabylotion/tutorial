import scrapy
from tutorial.items import TutorialItem
from scrapy.selector import Selector
from datetime import datetime, timedelta

TARGET_URL_BEFORE_CP = "http://media.daum.net/cp/"
TARGET_URL_BEFORE_PAGE = "?page="
TARGET_URL_REGDATE = "&regDate="

NEWS_CO = {11:"k", 45:"kk", 190:"d", 15:"m", 33:"s",
           38:"ss", 200:"j", 8:"jj", 17:"h", 49:"hh"}

class SpiderTest(scrapy.Spider):
    name = "getNews4"

    def start_requests(self):
        cpList = list(NEWS_CO.keys())

        endDate = '2017/03/25'
        end = datetime.strptime(endDate, "%Y/%m/%d")

        for cp in cpList:
            startDate = '2017/03/23'
            date = datetime.strptime(startDate, "%Y/%m/%d")

            while date != end:
                date += timedelta(days=1)
                st = datetime.strftime(date, "%Y/%m/%d")
                stRe = st.replace('/', '')

                for page in range(1, 2):
                    URL = TARGET_URL_BEFORE_CP + str(cp) + TARGET_URL_BEFORE_PAGE + str(
                        page) + TARGET_URL_REGDATE + stRe

                    yield scrapy.Request(url=URL, callback=lambda r, cp=cp, st=st:self.toParser(r, cp, st))

    def toParser(self, response,cp,st):
        aSelctor = Selector(response)
        urls = aSelctor.xpath('//ul[@class="list_news2 list_allnews"]/li/a/@href').extract()

        for url in urls:
            yield scrapy.Request(url=url, callback=lambda r, cp=cp, st=st:self.parse(r, cp, st))


    def parse(self, response,cp,st):
        hxs = Selector(response)

        selects = hxs.xpath('//div[@class="article_view"]//p/text()').extract()
        txt = ''.join(selects)
        if txt != "":
            item = TutorialItem()
            item['cp'] = cp
            item['aDate'] = st
            item['aTxt'] = txt

            yield item

    def closed(spider, reason):
        stats = spider.crawler.stats.get_stats()

        print('Spider closed:', spider.name, stats)
        print('Work time : ', stats['finish_time'] - stats['start_time'])












































