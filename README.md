
# Introduction
![Alt text](./sample.png?raw=true "sample_image")
<br/>
실시간 가장 핫한 키워드를 wordcloud로 시각화 해주는 프로그램
<br/>
<br/>

# How to install and run?
1. git clone https://github.com/Doohwancho/TrendSearch.py<br/>
2. pip3 install -r requirements.txt<br/>
3. python trendCloud.py<br/>

<br/>
<br/>
<br/>

# Update
ver 1.01<br/>
영어기사 제거, cmd창 숨김 기능 추가, 부팅시 자동시작 설정<br/>

ver 1.02<br/>
.exe(배포판 생성)은... 에러. 시도중.<br/>

ver 1.03<br/>
    1. dependencies -> requirements.txt<br/>
    2. refactor: depreciated code: webdriver.Chrome();<br/>
    3. refactor: relative path for AppleGothic.ttf font<br/>
    4. auto start on boot deleted due to inconveniency in setting<br/>

# Concepts

1. python virtual env
2. requirements.txt 
3. if __name__ == "__main__"
4. font library 호환성 
5. crawling 
6. html, css element 
7. regex
8. refactoring 
9. bat파일로 python 실행



# Library

1. selenium - crawling
2. beautifulsoup4 - crawling 
3. web driver manager - manipulate chrome
4. matplotlib - dependency for wordcloud
5. wordcloud - draw wordcloud


# More?

1. feat: wordcloud의 글자를 클릭하면, 관련 기사를 보여준다. 
