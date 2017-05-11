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
    name = "getNews"

    def getLink(self):
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

                    yield URL, st, cp

    def start_requests(self):
        aList = []
        aList = self.getLink()
        link = aList[0]
        st = aList[1]
        cp = aList[2]
#        link, st, cp = self.getLink()
        aSelctor = Selector(link)
        urls = aSelctor.xpath('//ul[@class="list_news2 list_allnews"]/li/a/@href').extract()

        for url in urls:
            yield scrapy.Request(st = st, cp = cp, url=url, callback=self.parse)


    def parse(self, response):
        hxs = Selector(response)
        selects =[]

        selects = hxs.xpath('//div[@class="article_view"]//p/text()').extract()
        txt = ''.join(selects)

        item = TutorialItem()
        item['cp'] = response.cp
        item['aDate'] = response.st
        item['aTxt'] = txt

        with('ttt.txt', 'wb') as f:
            f.write(txt)

        return item












































