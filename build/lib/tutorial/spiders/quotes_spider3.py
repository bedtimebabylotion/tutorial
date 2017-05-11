import scrapy
from tutorial.items import TutorialItem
from scrapy.selector import Selector
from datetime import datetime, timedelta

TARGET_URL_BEFORE_CP = "http://media.daum.net/cp/"
TARGET_URL_BEFORE_PAGE = "?page="
TARGET_URL_REGDATE = "&regDate="

NEWS_CO = {11:"경향신문", 45:"국민일보", 190:"동아일보", 15:"문화일보", 33:"서울신문",
           38:"세계일보", 200:"조선일보", 8:"중앙일보", 17:"한겨레", 49:"한국일보"}

class SpiderTest(scrapy.Spider):
    name = "getNews3"

    def start_requests(self):
        cpList = list(NEWS_CO.keys())

        endDate = '2016/02/24'
        end = datetime.strptime(endDate, "%Y/%m/%d")

        for cp in cpList:
            startDate = '2016/02/23'
            date = datetime.strptime(startDate, "%Y/%m/%d")

            while date != end:
                date += timedelta(days=1)
                st = datetime.strftime(date, "%Y/%m/%d")
                stRe = st.replace('/', '')

                for page in range(1, 2):
                    URL = TARGET_URL_BEFORE_CP + str(cp) + TARGET_URL_BEFORE_PAGE + str(
                        page) + TARGET_URL_REGDATE + stRe

                    yield scrapy.Request(url=URL, callback=self.parse)
    #
    # def toParser(self, response):
    #     aSelctor = Selector(response)
    #     urls = aSelctor.xpath('//ul[@class="list_news2 list_allnews"]/li/a/@href').extract()
    #
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        items=[]
        hxs = Selector(response)

        sites = hxs.select('//ul[@class="list_news2 list_allnews"]/li/a/@href').extract()

        for site in sites:
            item = TutorialItem()
            item['aTxt'] = site.select('//div[@class="article_view"]//p/text()').extract()
            items.append(item)

        return items












































