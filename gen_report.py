# Purpose: Generate research & meeting report automatically from website or blog
# Date: 2022.3.1
# Reference
#   https://www.scrapingbee.com/blog/crawling-python/
#   https://python-docx.readthedocs.io/en/latest/user/install.html

import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Inches
import argparse
import sys
import csv

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class auto_report:
    _url = ""
    _output = ""
    _begin = 0
    _dist = 0
    _step = 0
    _header = []
    _body_title = []

    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def generate_body(self, html, begin = 2000, dist = 500, step = 2000, cnt = 1):
        print("Research Note")
        soup = BeautifulSoup(html, 'html.parser')

        body = ""
        index = 0
        for b in soup.find_all('body'):
            t = b.text
            t = t.replace("\n", "")

            b = begin
            if b >= len(t):
                b = 0
            if dist <= 0:
                dist = len(t) - b - 1

            current = 0
            while (b + dist + step) < len(t):
                t2 = t[b: b + dist]

                if current >= len(self._body_title):
                    current = 0
                t2 = self._body_title[current] + "\n" + t2 + "...\n\n"
                print(t2)
                body = body + t2
                b = b + dist + step
                print("begin = ", b)
                current = current + 1

            if index >= cnt:
                break
            index = index + 1
        return body

    def crawl(self, url):
        html = self.download_url(url)
        body = self.parsing_body(html)

    def createWord(self, fname = "out.docx", body = "Hello world!"):
        document = Document()
        document.add_heading('연구노트', 0)

        table = document.add_table(rows=3, cols=5)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = '현황'
        hdr_cells[1].text = '소속'
        hdr_cells[2].text = self._header[0]
        hdr_cells[3].text = '직급'
        hdr_cells[4].text = self._header[1]
        hdr_cells = table.rows[1].cells
        hdr_cells[1].text = '사번'
        hdr_cells[2].text = self._header[2]
        hdr_cells[3].text = '성명'
        hdr_cells[4].text = self._header[3]
        hdr_cells = table.rows[2].cells
        hdr_cells[1].text = '일자'
        hdr_cells[2].text = self._date
        hdr_cells[3].text = '근무시간/장소'
        hdr_cells[4].text = self._header[4]

        table = document.add_table(rows=3, cols=2)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = '주요수행업무'
        hdr_cells[1].text = body
        hdr_cells = table.rows[1].cells
        hdr_cells[0].text = '이동현황'
        hdr_cells[1].text = '-'
        hdr_cells = table.rows[2].cells
        hdr_cells[0].text = '기타사항'
        hdr_cells[1].text = '-'

        table = document.add_table(rows=1, cols=5)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = '확인'
        hdr_cells[1].text = '부서(직책)'
        hdr_cells[2].text = self._header[0]
        hdr_cells[3].text = '성명'
        hdr_cells[4].text = self._header[3] + ' (서명)'

        # document.add_page_break()
        document.save(fname)

if __name__ == '__main__':
    url = 'https://sites.google.com/site/bimprinciple/in-the-news/gieob-uidijiteoljeonhwanguhyeon'
    # url = 'http://daddynkidsmakers.blogspot.com/2022/02/floor-plan.html'

    c = auto_report()
    if len(sys.argv) >= 7:
        c._date = sys.argv[1]
        c._url = sys.argv[2]
        c._output = sys.argv[3]
        c._begin = int(sys.argv[4])
        c._dist = int(sys.argv[5])
        c._step = int(sys.argv[6])

    index = 0
    with open("config.csv", 'r', encoding = 'UTF-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if index == 0:
                c._header = row
            if index == 1:
                c._body_title = row 
            index = index + 1

    print(c._header)        
    print(c._body_title)        

    html = c.download_url(c._url)
    body = c.generate_body(html, c._begin, c._dist, c._step)
    c.createWord(c._output, body)
