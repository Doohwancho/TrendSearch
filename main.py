import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from numpy import number
from bs4 import BeautifulSoup
from wordcloud import WordCloud
from config import *
import matplotlib.pyplot as plt
import re
import time


def get_last_page_number():
    # Initial request to find the max_page_number
    initial_url = 'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=001&listType=summary&date=20240221&page=10000'
    response = requests.get(initial_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        pagination_strong_tag = soup.select_one('.paging strong')
        if pagination_strong_tag:
            max_page_number = int(pagination_strong_tag.text.strip())
            print(f"Max page number: {max_page_number}")
            return max_page_number
        else:
            print("Could not find the last pagination number.")
            return
    else:
        print(f"Failed to retrieve the initial page. Status code: {response.status_code}")
        return


def fetch_page(page_number):
    """
    Fetch and parse a single page, returning the titles found.
    """
    url = f'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=001&listType=summary&date=20240221&page={page_number}'
    response = requests.get(url)
    titles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        titles1 = soup.select('.newsflash_body .type06_headline li dl dt:not(.photo) a')
        titles2 = soup.select('.newsflash_body .type06 li dl dt:not(.photo) a')
        titles = [title.get_text(strip=True) for title in titles1 + titles2]
    else:
        print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")

    return titles



def customFilter(words, filtering_words):
    return [word for word in words if all(word not in censor for censor in filtering_words)]

def regExp(rawData):
    arrayToString = ''.join(rawData) #array to string
    refinedData = re.sub(r'\s+', ' ', arrayToString).strip().replace('\n', '').replace('\t', '') #string to string
    koreanFiltered = re.findall(r'\b[가-힣]{2,15}\b', refinedData) #string to array
    filteredKoreanWords = customFilter(koreanFiltered, FILTERING_WORDS)

    return filteredKoreanWords

def wordCloud(koreanWords):
    wordcloud = WordCloud(font_path=FONT_PATH, max_words=MAX_WORDS, background_color=BACKGROUND_COLOR, width=WIDTH_SIZE, height=HEIGHT_SIZE).generate(' '.join(koreanWords))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    return

def main():
    # max_page_number = get_last_page_number()
    max_page_number = NUMBER_OF_PAGES_TO_CRAWL

    all_titles = []  # Initialize an empty list to hold all titles

    # Crawl pages in parallel
    with ThreadPoolExecutor() as executor:
        # Submit all fetch tasks and create a future-to-page mapping
        future_to_page = {executor.submit(fetch_page, page_number): page_number for page_number in range(1, max_page_number + 1)}

        # Process the results as they complete
        for future in as_completed(future_to_page):
            page_number = future_to_page[future]
            try:
                titles = future.result()
                all_titles.extend(titles)  # Extend the all_titles list with the titles from this page
                # print(f"Page {page_number} titles fetched")
            except Exception as exc:
                print(f"Page {page_number} generated an exception: {exc}")


    # filter words
    filteredKoreanWords = regExp(all_titles)

    # draw wordcloud
    wordCloud(filteredKoreanWords)

if __name__ == "__main__":
    main()
