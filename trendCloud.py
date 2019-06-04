from selenium import webdriver
from bs4 import BeautifulSoup
import re
import operator
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import time


def chromeDriverSetting():
    global path
    #chrome driver 설정(headless : 팝업창 없는 크롤링)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome(path, options=options)
    return driver

def regExp(rawData):
    Stringtype = ''.join(rawData)
    Stringtype = re.sub(r'\s+', ' ', Stringtype).strip().replace('\n', '').replace('\t', '')
    Stringtype = Stringtype.replace('"', '').replace("'", '').replace("동영상기사", '').replace("사진", '')\
                  .replace("포토",'').replace('한경로보뉴스', '').replace('뉴스', '').replace('[', '')\
                  .replace(']', '').replace("속보","").replace("오늘","").replace("오늘의","")
    koreanWords = re.findall(r'\b[가-힣]{2,15}\b', Stringtype)
    return koreanWords

def wordCloud(koreanWords):
    wordcloud = WordCloud(font_path='C:\Windows\Fonts\Applegothic.ttf',
                         background_color='white', width=1600, height=1200).generate(' '.join(koreanWords))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    return

def crawler(driver, rawData, start = 2, end = 12):
    for i in range(start, end):
        s1 = driver.page_source
        s2 = BeautifulSoup(s1, "html.parser")
        s3 = s2.find("ul", class_="type06_headline")
        s4 = s3.find_all("a", class_="nclicks(fls.list)")

        for j in s4:
            rawData.append(j.text)

        driver.find_element_by_css_selector("#main_content > div.paging > a:nth-child(" + str(i) + ")").click()

    return driver


def crawling(driver):
    try:
        global crawlingPage
        rawData = []
        driver.get("https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=001")

        driver = crawler(driver,rawData)
        while crawlingPage > 1:
            crawler(driver, rawData, 3,13)
            crawlingPage -= 1

        return rawData

    except:
        print("인터넷이 연결되어 있지 않거나, 새벽 12시가 지나 네이버 기사가 초기화 되어, 입력한값 만큼의 기사가 없습니다.")
        print("")
        print("30초 후 재시작합니다.")

    finally:
        driver.close()

def trendSearch():
    global condition
    driver = chromeDriverSetting()
    rawData = crawling(driver)
    koreanWords = regExp(rawData)
    wordCloud(koreanWords)
    condition = False
    return


if __name__ == "__main__":
    condition = True
    crawlingPage = 2  # 1당 10페이지(신문기사 제목 200개) 크롤링
    path = "**Insert path to chromedriver.exe**" #크롬 드라이버 path 설정

    while True:
        try:
            trendSearch()
        except:
            pass
        time.sleep(30)
        if condition: continue
        break
