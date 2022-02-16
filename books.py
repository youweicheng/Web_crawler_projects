from bs4 import BeautifulSoup
import bs4
import requests
from lxml import etree
import json


class BookSpider(object):

    def __init__(self):

        self.basic_url = "https://www.books.com.tw/web/cebook_new/?o=1&v=1&page={}"

        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
                        }

        self.book_data = []


    def get_response(self, url):

        data = requests.get(url, headers=self.headers).content.decode("utf-8")

        # print(data)

        return data

    def parse_data_xpath(self, data):

        data_xpath = etree.HTML(data)

        book_title = data_xpath.xpath('//div[@class="item"]')

        print(len(book_title))



        for book in book_title:

            book_dict = {}

            book_dict["book_name"] = book.xpath('.//div[@class = "msg"]/h4/a/text()')[0]
            # print(book_dict)
            book_dict["book_author"] = book.xpath('.//div[@class = "msg"]//li[@class = "info"]/a/text()')[0]
            # print(book_dict)
            book_dict["book_pic"] = book.xpath('.//a/img/@src')[0]
            # print(book_dict)
            try:
                book_dict["book_info"] = (book.xpath('.//p/text()'))[0]
            except IndexError:
                book_dict["book_info"] = "no info"




            self.book_data.append(book_dict)
            # print(self.book_data)
    def parse_data_bs4(self, data):

        soup = bs4.BeautifulSoup(data, "lxml")

        book_list = soup.select("div.item")



        for book in book_list:

            book_dict = {}
            try:
                book_dict["book_name"] = book.select_one("div.msg a").get_text()
            except AttributeError:
                break

            book_dict["book_author"] = book.select_one("li.info a").get_text()

            book_dict["book_info"] = book.select_one("div.txt_cont p").get_text()

            book_dict["book_pic"] = book.select_one(".cover").get('src')

            print(book_dict)

            self.book_data.append(book_dict)






    def save_data(self,data):

        # json.dump(self.book_data, open("book_json.json", "w"))
        with open("book.html", "w")as f:
            f.write(data)
    def run(self):

        for i in range(1,2):

            url = self.basic_url.format(i)

            data = self.get_response(url)
            # self.parse_data_xpath(data)
            self.parse_data_bs4(data)
        self.save_data(data)

    # def get_url_list(self):
    #
    #     url_list = []
    #
    #     self.basic_url = "https://www.books.com.tw/web/cebook_new/?o=1&v=1&page={}"
    #
    #     for i in range(1,2):
    #         url = self.basic_url.format(i)
    #         url_list.append(url)
    #     return url_list



BookSpider().run()


