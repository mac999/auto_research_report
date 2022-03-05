# Auto Research Note
Research report generation automatically

# purpose
자동으로 연구노트를 생성하는 파이썬 프로그램. 
기술개발 블로그에서 다시 연구노트 문서로 만들기 귀찬아, 연구행정간소화 차원에서 만든 프로그램. 
검색식이나 웹사이트 명령행에 입력하면 해당 컨텐츠 크롤링해 옵션에 맞게 연구 메모 텍스트 만들어 워드파일로 생성.
다음과 같이 자주 사용하거나 글을 쓰는 웹사이트나 검색식을 지정하면, 자동으로 크롤링해서 연구노트 워드파일을 생성함. - 과도한 행정에 지친 연구자를 위해 

다음과 같이 실행하면 됨.<br>
python gen_report.py 2022/1/4 "computer science" r3.docx 100 300 50

<img src = "https://github.com/mac999/auto_research_report/blob/main/demo.PNG" width="70%"/>

# function
1. Command arguments
python gen_report.py [date] ["Google query keyword" or URL] output.docx begin length step

begin = begin position of content text</br>
length = copy character length</br>
step = skip character length</br>

2. config.csv includes document header, title like below. <br>

R&D, Research Fellow, 12, mac, office <br>
*문헌조사내용(일부),*주요연구내용(일부),*관련연구,*핵심사항,*아이디어,*요점 <br>

# Install development environment in Windows
1. <a href="https://docs.anaconda.com/anaconda/install/">Install Anaconda</a>
2. Open Anaconda terminal 

# Install development environment in Ubuntu
1. <a href="https://www.python.org/downloads/">install python</a>
2. <a href="https://pip.pypa.io/en/stable/installation/">install pip</a>

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
https://www.scrapingbee.com/blog/crawling-python/<br>
https://python-docx.readthedocs.io/en/latest/user/install.html
