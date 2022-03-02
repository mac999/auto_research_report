# auto_research_report
Research report generation automatically

# purpose
자동으로 연구노트를 생성하는 파이썬 프로그램. 
다음과 같이 자주 사용하거나 글을 쓰는 웹사이트나 검색식을 지정하면, 자동으로 크롤링해서 연구노트 워드파일을 생성함. - 과도한 행정에 지친 연구자를 위해 

다음과 같이 실행하면 됨. 
python gen_report.py 2022/1/4 "computer science" r3.docx 100 300 50

<img src = "https://github.com/mac999/auto_research_report/blob/main/demo.PNG" width="70%"/>

# function
Command arguments
python gen_report.py [date] ["Google query keyword" or URL] output.docx begin length step

begin = begin position of content text</br>
length = copy character length</br>
step = skip character length</br>

# Install development environment in Windows
1. Install Anaconda
2. Open Anaconda terminal 

# Install development environment in Ubuntu
1. install python
2. install pip

# Install packages
Open terminal and Input the below pip install commands</br></br>
pip install beautifulsoup4</br>
pip install requests bs4</br>
pip install google</br>
pip install python-docx</br>

# example
python gen_report.py 2022/1/2 https://sites.google.com/site/bimprinciple/in-the-news/gieob-uidijiteoljeonhwanguhyeon r1.docx 2000 300 2000<br>
python gen_report.py 2022/1/3 http://daddynkidsmakers.blogspot.com/2022/02/pdal-3.html r2.docx 1000 200 50<br>
python gen_report.py 2022/1/4 "computer science" r3.docx 100 300 50<br>

# reference
https://www.scrapingbee.com/blog/crawling-python/
https://python-docx.readthedocs.io/en/latest/user/install.html
