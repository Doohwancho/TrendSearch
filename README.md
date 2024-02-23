
# Introduction
![Alt text](./sample.png?raw=true "sample_image")
<br/>
실시간 가장 핫한 키워드를 네이버 뉴스에서 크롤링 해서 wordcloud로 시각화 해주는 프로그램
<br/>
<br/>

# How to install and run?

prerequisites: python 3.8
```
git clone https://github.com/Doohwancho/TrendSearch
cd TrendSearch
pip3 install -r requirements.txt
python main.py
```


<br/>

# Update

## ver 1.08
1. feat: 영어기사 제거
2. feat: crawling 도중 command 창 숨김 기능 추가
3. optimization: chrome driver options
4. build: dependencies -> requirements.txt
5. refactor: depreciated code: webdriver.Chrome();
6. refactor: configuration option separated into config.py
7. refactor: relative path for AppleGothic.ttf font
8. fix: selenium >= 4.10.0 supports Service that takes care of downloading latest compatible chrome driver
9. fix: DEPRECATED - selenium 4.18.1 does not support find_element_by_css_selector()
