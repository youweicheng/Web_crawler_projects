import requests
from lxml import etree
from bs4 import BeautifulSoup
import json


class BookSpider(object):
    def __init__(self):
        self.base_url = 'http://www.allitebooks.com/page/{}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }

        self.data_list = []

    # 1.构建所有url
    def get_url_list(self):
        url_list = []
        for i in range(1, 2):
            url = self.base_url.format(i)

            url_list.append(url)

        return url_list

    # 2.发请求
    def send_request(self, url):
        data = requests.get(url, headers=self.headers).content.decode()
        print(url)
        return data

    # 3.解析数据 xpath
    def parse_xpath_data(self, data):
        parse_data = etree.HTML(data)

        # 1.解析出所有的书 book
        book_list = parse_data.xpath('//div[@class="main-content-inner clearfix"]/article')

        # 2.解析出 每本书的 信息
        for book in book_list:
            
            book_dict = {}
            # 1.书名字
            book_dict['book_name'] = book.xpath('.//h2[@class="entry-title"]//text()')[0]

            # 2.书的图片url
            book_dict['book_img_url'] = book.xpath('div[@class="entry-thumbnail hover-thumb"]/a/img/@src')[0]

            # 3.书的作者
            book_dict['book_author'] = book.xpath('.//h5[@class="entry-author"]//text()')[0]

            # 4.书的简介
            book_dict['book_info'] = book.xpath('.//div[@class="entry-summary"]/p/text()')[0]

            self.data_list.append(book_dict)

    def parse_bs4_data(self, data):

        bs4_data = BeautifulSoup(data, 'lxml')
        # 1.取出所有的书
        book_list = bs4_data.select('article')

        # 2.解析出 每本书的 信息
        for book in book_list:
            book_dict = {}
            # 1.书名字
            book_dict['book_name'] = book.select_one('.entry-title').get_text()

            # # 2.书的图片url
            book_dict['book_img_url'] = book.select_one('.attachment-post-thumbnail').get('src')

            # # 3.书的作者
            book_dict['book_author'] = book.select_one('.entry-author').get_text()[3:]
            #
            # # 4.书的简介
            book_dict['book_info'] = book.select_one('.entry-summary p').get_text()
            print(book_dict)
            self.data_list.append(book_dict)

    # 4.保存数据
    def save_data(self):
        json.dump(self.data_list, open("04book.json", 'w'))

    # 统筹调用
    def start(self):

        url_list = self.get_url_list()

        # 循环遍历发送请求
        for url in url_list:
            data = self.send_request(url)
            # self.parse_xpath_data(data)
            self.parse_bs4_data(data)

        self.save_data()


BookSpider().start()
