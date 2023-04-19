from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from wordcloud import WordCloud
from config import *
import matplotlib.pyplot as plt
import re
import time

def get_chrome_options():
    options = webdriver.ChromeOptions()

    if HIDE_BROWSER_WHILE_CRAWLING:
        options.add_argument('headless')

    options.add_argument('window-size=1920x1080')
    options.add_argument("--no-sandbox")
    options.add_argument("disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")

    return options

def chromeDriverSetting():
    options = get_chrome_options()
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(f"Error while installing ChromeDriver: {e}")
        exit()

    return driver

def customFilter(words, filtering_words):
    return [word for word in words if all(word not in censor for censor in filtering_words)]

def regExp(rawData):
    arrayToString = ''.join(rawData) #array to string
    refinedData = re.sub(r'\s+', ' ', arrayToString).strip().replace('\n', '').replace('\t', '') #string to string
    koreanFiltered = re.findall(r'\b[가-힣]{2,15}\b', refinedData) #string to array
    filteredKoreanWords = customFilter(koreanFiltered, FILTERING_WORDS)

    return filteredKoreanWords

def wordCloud(koreanWords):
    wordcloud = WordCloud(font_path=FONT_PATH, max_words=MAX_WORDS,
                         background_color=BACKGROUND_COLOR, width=WIDTH_SIZE, height=HEIGHT_SIZE).generate(' '.join(koreanWords))
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
        numberOfPageToCrawl = CRAWLING_PAGE
        rawData = []
        driver.get("https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=001")

        driver = crawler(driver,rawData)
        while numberOfPageToCrawl > 1:
            crawler(driver, rawData, 3,13)
            numberOfPageToCrawl -= 1

        return rawData
    except:
        print("인터넷이 연결되어 있지 않거나, 새벽 12시가 지나 네이버 기사가 초기화 되어, 입력한값 만큼의 기사가 없습니다.")
    finally:
        driver.close()
        driver.quit()


def main():
    driver = None
    try:
        driver = chromeDriverSetting()
        rawData = crawling(driver)
        filteredKoreanWords = regExp(rawData)
        wordCloud(filteredKoreanWords)
    except Exception as e:
        print("예외가 발생했습니다.", e)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

