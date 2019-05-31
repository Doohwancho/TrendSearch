from selenium import webdriver
from bs4 import BeautifulSoup
import re
import operator
import matplotlib.pyplot as plt
from wordcloud import WordCloud

#chrome driver 설정
driver = webdriver.Chrome("**NEED CHROME DRIVER'S PATH**")
driver.get("https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=001")

global rawData
rawData = []

def WordCount(t):
    frequency = {}
    wordcount = {}
    match_pattern = t

    for word in match_pattern:
        count = frequency.get(word, 0)
        frequency[word] = count + 1

    frequency_list = frequency.keys()
    wordCloudWords = []
    for words in frequency_list:
        wordcount.update({words: frequency[words]})
        wordcount2 = sorted(wordcount.items(), key=operator.itemgetter(1), reverse=True)
        wordCloudWords.append(words)
    return ([wordcount2[i] for i in range(1, 31)])


try:
    for i in range(2, 12):  # 2 12
        s1 = driver.page_source
        s2 = BeautifulSoup(s1, "html.parser")
        s3 = s2.find("ul", class_="type06_headline")
        s4 = s3.find_all("a", class_="nclicks(fls.list)")

        for j in s4:
            rawData.append(j.text)

        driver.find_element_by_css_selector("#main_content > div.paging > a:nth-child(" + str(i) + ")").click()

        if (i == 11):
            for x in range(1, 2): #1 10    #만약 해당 페이지 이후가 없으면 넘어가도록 exception 처리 필요
                for a in range(3, 13): #3 13
                    s1 = driver.page_source
                    s2 = BeautifulSoup(s1, "html.parser")
                    s3 = s2.find("ul", class_="type06_headline")
                    s4 = s3.find_all("a", class_="nclicks(fls.list)")

                    for b in s4:
                        rawData.append(b.text)

                    driver.find_element_by_css_selector("#main_content > div.paging > a:nth-child(" + str(a) + ")").click()

    Stringtype = ''.join(rawData)
    Stringtype = re.sub(r'\s+', ' ', Stringtype).strip().replace('\n', '').replace('\t', '')
    Stringtype = Stringtype.replace('"', '').replace("'", '').replace("동영상기사", '').replace("사진", '').replace("포토",
                                                                                                             '').replace(
        '한경로보뉴스', '').replace('뉴스', '').replace('[', '').replace(']', '')
    korean = re.findall(r'\b[가-힣]{2,15}\b', Stringtype)

    SortedWords = (WordCount(korean))
    print("------sorted words-------")
    print(SortedWords)
    print("-------------------------")

    wordcloud = WordCloud(font_path='C:\Windows\Fonts\Applegothic.ttf',
                          background_color='white', width=4000, height=3200).generate(' '.join(korean))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

finally:
    driver.close()
