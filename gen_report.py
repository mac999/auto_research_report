# Purpose: Generate research & meeting report automatically from website or blog
# Date: 2022.3.1
# Author: mac999
# 

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
    _urls = []
    _output = ""
    _begin = 0
    _dist = 0
    _step = 0
    _header = []
    _body_title = []

    def download_url(self, url):
        return requests.get(url).text

    def searchGoogle(self, query):
        try:
            from googlesearch import search
        except ImportError:
            print("No module named 'google' found")

        for u in search(query, tld="co.in", num=10, stop=10, pause=2):
            print(u)
            self._urls.append(u)

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def is_empty_content(self, txt, ratio = 0.7):
        space = txt.count(' ')    
        r = 1.0 - float(space) / float(len(txt))
        if r < ratio:
            return True
        return False

    def generate_body(self, html, begin = 2000, dist = 500, step = 2000, cnt = 1):
        print("\nResearch Note")
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
                b = b + dist + step

                if self.is_empty_content(t2):
                    continue

                if current >= len(self._body_title):
                    break
                t2 = self._body_title[current] + "\n" + t2 + "...\n\n"
                print(t2)
                body = body + t2
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
        document.add_heading('Research Note', 0)

        table = document.add_table(rows=3, cols=4)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Department'
        hdr_cells[1].text = self._header[0]
        hdr_cells[2].text = 'Position'
        hdr_cells[3].text = self._header[1]
        hdr_cells = table.rows[1].cells
        hdr_cells[0].text = 'ID'
        hdr_cells[1].text = self._header[2]
        hdr_cells[2].text = 'Name'
        hdr_cells[3].text = self._header[3]
        hdr_cells = table.rows[2].cells
        hdr_cells[0].text = 'Date'
        hdr_cells[1].text = self._date
        hdr_cells[2].text = 'Place'
        hdr_cells[3].text = self._header[4]

        table = document.add_table(rows=2, cols=1)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Note'
        hdr_cells = table.rows[1].cells
        hdr_cells[0].text = body

        table = document.add_table(rows=1, cols=5)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Confirmation'
        hdr_cells[1].text = 'Position'
        hdr_cells[2].text = self._header[0]
        hdr_cells[3].text = 'Name'
        hdr_cells[4].text = self._header[3] + ' (Sign)'

        # document.add_page_break()
        document.save(fname)

if __name__ == '__main__':
    url = 'https://sites.google.com/site/bimprinciple/in-the-news/gieob-uidijiteoljeonhwanguhyeon'
    # url = 'http://daddynkidsmakers.blogspot.com/2022/02/floor-plan.html'

    c = auto_report()
    if len(sys.argv) >= 7:
        c._date = sys.argv[1]
        c._urls.append(sys.argv[2])
        if sys.argv[2].find('http') < 0:
            print("Knowledge searching mode...")
            c._urls.clear()
            c.searchGoogle("computer science")

        c._output = sys.argv[3]
        c._begin = int(sys.argv[4])
        c._dist = int(sys.argv[5])
        c._step = int(sys.argv[6])

    print("\nReading config file...")
    index = 0
    with open("config.csv", 'r', encoding = 'UTF-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if index == 0:
                c._header = row
            if index == 1:
                c._body_title = row 
            index = index + 1

    print("\nProcessing...")
    print(c._header)        
    print(c._body_title)        

    html = c.download_url(c._urls[0])
    body = c.generate_body(html, c._begin, c._dist, c._step)
    c.createWord(c._output, body)
