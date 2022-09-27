from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import time


def chromeDriverSetting():
    #chrome driver 설정(headless : 팝업창 없는 크롤링)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def customFilter(string, filtering_words):
    return [str for str in string if all(str not in sub for sub in filtering_words)]

def regExp(rawData):
    arrayToString = ''.join(rawData)
    refinedData = re.sub(r'\s+', ' ',arrayToString).strip().replace('\n', '').replace('\t', '')
    koreanFiltered = re.findall(r'\b[가-힣]{2,15}\b', refinedData)
    filtering_words = ['동영상','기사','동영상기사','사진','포토','뉴스','오늘','속보']
    filteredKoreanWords = customFilter(koreanFiltered, filtering_words)

    return filteredKoreanWords

def wordCloud(koreanWords):
    print(koreanWords)
    wordcloud = WordCloud(font_path='Applegothic.ttf',
                         background_color='white', width=1600, height=1200).generate(' '.join(koreanWords)) #error: 여기에서 안넘어감
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
        # driver.find_element(by=By.CSS_SELECTOR, value="#main_content > div.paging > a:nth-child(" + str(i) + ")").click()

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
        print("10초 후 재시작합니다.")

    finally:
        driver.close()

def trendSearch():
    global condition
    driver = chromeDriverSetting()
    rawData = crawling(driver)
    filteredKoreanWords = regExp(rawData)
    wordCloud(filteredKoreanWords)
    condition = False
    return


if __name__ == "__main__":
    condition = True
    crawlingPage = 3  # 1당 10페이지(신문기사 제목 200개) 크롤링

    while condition:
        try:
            trendSearch()
        except:
            pass
        time.sleep(10)
