import re

import requests
import scrapy  # 导入scrapy包
from bs4 import BeautifulSoup
from scrapy.http import Request  ##一个单独的request的模块，需要跟进URL的时候，需要用它
from spider1.items import BdlvSpiderItem  ##这是我定义的需要保存的字段，（导入dingdian项目中，items文件中的DingdianItem类）

class Myspider(scrapy.Spider):
    name = 'spider1'
    allowed_domains = ['tuniu.com']
    bash_url = 'www.tuniu.com/domestic/'
    bashurl = '.html'
    urls=[]



    def start_requests(self):
        # for i in range(1, 11):
        #     url = self.bash_url + str(i) + '_1' + self.bashurl
        #     yield Request(url, self.parse)
        # yield Request('http://www.23wx.com/quanben/1', self.parse)
        yield Request('http://s.tuniu.com/search_complex/', self.parse)

    def parse(self, response):
        print(response.text)
        # citys = response.xpath('//h4[@class="hsb_tt"]//a/text()').extract()
        # print(citys)
        urls=response.xpath('//div[@class="hsb_list"]//a/@href').extract()
        print(urls)
        print(len(urls))
        for url in urls:
            print(url)
            html = self.got_html(url)
            # self.parse_html(content)
            soup = BeautifulSoup(html, 'lxml')
            item_list = soup.select('ul[class="thebox clearfix"] li')
            # print(len(item_list))
            for item in item_list:
                # 名称
                namelist = item.select('div > a > dl > dt > p.title > span')
                if len(namelist) != 0:
                    name = namelist[0].get_text().strip()
                else:
                    name = 0;

                # 价格
                princelist = item.select('div > a > div.priceinfo > div.tnPrice > em')
                if len(princelist) != 0:
                    price = princelist[0].get_text().strip()
                else:
                    price = 0

                # 满意度
                doslist = item.select(
                    'div > a > div.priceinfo > div.comment-sat.clearfix > div.comment-satNum > span > i')
                if len(doslist) != 0:
                    dos = doslist[0].get_text().strip()
                else:
                    dos = 0

                # 出游人数
                numlist = \
                    item.select(
                        'div > a > div.priceinfo > div.comment-sat.clearfix > div.trav-person > p.person-num > i')
                if len(numlist) != 0:
                    number = numlist[0].get_text().strip()
                else:
                    number = 0
                Item=BdlvSpiderItem()
                Item['name'] = name
                Item['price'] = price
                Item['dos'] = dos
                Item['number'] = number
                print(name, price, dos, number)
                yield Item



    def parse_html(self, html):

        soup = BeautifulSoup(html, 'lxml')
        item_list = soup.select('ul[class="thebox clearfix"] li')
        # print(len(item_list))
        for item in item_list:
            # 名称
            namelist=item.select('div > a > dl > dt > p.title > span')
            if len(namelist)!=0:
                name = namelist[0].get_text().strip()
            else:
                name = 0;

            # 价格
            princelist = item.select('div > a > div.priceinfo > div.tnPrice > em')
            if len(princelist) != 0:
                price = princelist[0].get_text().strip()
            else:
                price = 0

            # 满意度
            doslist=item.select('div > a > div.priceinfo > div.comment-sat.clearfix > div.comment-satNum > span > i')
            if len(doslist) != 0:
                dos = doslist[0].get_text().strip()
            else:
                dos = 0

            # 出游人数
            numlist = \
                item.select('div > a > div.priceinfo > div.comment-sat.clearfix > div.trav-person > p.person-num > i')
            if len(numlist) != 0:
                number = numlist[0].get_text().strip()
            else:
                number = 0
            BdlvSpiderItem['name']=name
            BdlvSpiderItem['price']=price
            BdlvSpiderItem['dos']=dos
            BdlvSpiderItem['number']=number
            print(name, price, dos, number)
            yield BdlvSpiderItem

    def got_html(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/69.0.3497.100 Safari/537.36'}
        # url = 'http://s.tuniu.com/search_complex/whole-nj-0-%E6%B3%B0%E5%9B%BD/'
        response = requests.get(url, headers=headers)
        html = response.content.decode()
        # print(html)
        return html