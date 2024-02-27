from numpy import number
from selenium import webdriver
from selenium.webdriver.common.by import By
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
    service = Service()
    options = get_chrome_options()
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=options)
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

def crawler(driver, rawData, number_of_pages_to_crawl = 1):
    for i in range(0, number_of_pages_to_crawl):
        s1 = driver.page_source
        s2 = BeautifulSoup(s1, "html.parser")
        s3 = s2.find("ul", class_="type06_headline")
        s4 = s3.find_all("a", class_="nclicks(fls.list)")

        if(i >= 10):
            i += 1; # 11페이지 부터는 '이전' 버튼이 생기기 때문에 +1을 해준다.
        next_page_selector = "#main_content > div.paging > a:nth-child({})".format((i%10)+2) # first child is <strong>1</strong>. therefore, skip. second child is current page. therefore, skip.

        for j in s4:
            # Check if the <a> tag contains an <img> tag
            if j.find('img') is None:
                # If no <img> tag is found, extract the title
                text = j.get_text(strip=True)
                rawData.append(text)

        driver.find_element(By.CSS_SELECTOR, next_page_selector).click()

    return driver


def crawling(driver):
    try:
        rawData = []
        number_of_pages_to_crawl = NUMBER_OF_PAGES_TO_CRAWL
        driver.get("https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=001")
        driver = crawler(driver, rawData, number_of_pages_to_crawl)

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

