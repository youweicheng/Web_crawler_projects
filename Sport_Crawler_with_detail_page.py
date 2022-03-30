import requests
from bs4 import BeautifulSoup
import json
from lxml import etree
import re

class Detail_SportCrawler(object):

    def __init__(self):

        self.url = "https://www.playsport.cc/forum.php?pageno={}"

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        }

        self.data_list = []

        self.data_detail = []

        self.answer_list = []

    def get_response(self, url):

        free_proxy = {'http': '20.88.122.67:8080'}

        data = requests.get(url, headers=self.headers, proxies=free_proxy).content

        return data

    def parse_data(self, data):

        soup = BeautifulSoup(data, 'lxml')

        result = soup.select('span a')

        # print(result)

        for contents in result:

            data_dict = dict()

            data_dict['title'] = contents.get_text()

            data_dict['url'] = "https://www.playsport.cc/" + contents.get('href')

            self.data_list.append(data_dict)


    def parse_detail_data(self, data):

        detail_soup = BeautifulSoup(data, 'lxml')

        detail_title = re.findall(r'\w*\s*[\u4e00-\u9fa5]*\?*', detail_soup.select('.title')[0].get_text())
        # print(detail_title)

        detail_title_str = ""

        for word in detail_title:

            detail_title_str += word
            # only title, no category
            # detail_title_str.split("\n")[-1].strip()

        adj_detail_title_str = detail_title_str.replace("\n", "").replace("     ", ":")

        xpath_data = etree.HTML(data)

        answers = xpath_data.xpath('//td/text()')

        answers_str = ""

        for word in answers:

            answers_str += word

        answers_str_all = answers_str.replace("\n", "").strip(" ").replace(" ", "")

        answers_list_floor = re.findall(r'(\d+\u6a13)', answers_str_all)
        # lack of first floor, so add it by hand
        answers_list_floor.insert(0, "1樓")

        answers_str_comment = re.sub(r'(\d+\u6a13)', '\n', answers_str_all).replace("r", "")

        answers_list_comment = answers_str_comment.split("\n")

        answers_list_combined = list(zip(answers_list_floor, answers_list_comment))

        answers_dict = {
            "title": adj_detail_title_str,
            "answer": answers_list_combined
        }

        self.data_detail.append(answers_dict)

        print(self.data_detail)

    def save_data(self, data, filepath):

        data_str = json.dumps(data)

        with open(filepath, "w") as f:

            f.write(data_str)

    def run(self):

        for i in range(1, 2):

            url = self.url.format(i)

            data = self.get_response(url)

            self.parse_data(data)

        self.save_data(self.data_list, "title.json")

        for data in self.data_list:

            detail_url = data['url']

            if detail_url == "https://www.playsport.cc/https://www.playsport.cc/visit_member.php?pagetype=predict&visit=a0986076126&allianceid=92&gameday=today&from=cons&path_trace=cD1GUkxfQztjPeWThuWVpueMtOWkoiDpn5PnsYMg5ZyL6Zqb55uk6L-RMjjml6UgMzLpgY4yNA&rp=FRL_C":
                
                pass

            detail_data = self.get_response(detail_url)

            self.parse_detail_data(detail_data)

        self.save_data(self.data_detail, "detail.json")


Detail_SportCrawler().run()





