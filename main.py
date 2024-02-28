import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
from wordcloud import WordCloud
from config import *
import matplotlib.pyplot as plt
import re
from collections import defaultdict
from operator import itemgetter
import argparse

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

def crawling_parallel(date_to_crawl):
    max_page_number = NUMBER_OF_PAGES_TO_CRAWL

    all_titles = []  # Initialize an empty list to hold all titles

    # Crawl pages in parallel
    with ThreadPoolExecutor() as executor:
        # Submit all fetch tasks and create a future-to-page mapping
        future_to_page = {executor.submit(fetch_page, page_number, date_to_crawl): page_number for page_number in range(1, max_page_number + 1)}

        # Process the results as they complete
        for future in as_completed(future_to_page):
            page_number = future_to_page[future]
            try:
                titles = future.result()
                all_titles.extend(titles)  # Extend the all_titles list with the titles from this page
                # print(f"Page {page_number} titles fetched")
            except Exception as exc:
                print(f"Page {page_number} generated an exception: {exc}")

    crawled_data_in_string = ' '.join(all_titles)

    return crawled_data_in_string


def fetch_page(page_number, date_to_crawl):
    """
    Fetch and parse a single page, returning the titles found.
    """
    url = f'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=001&listType=summary&date={date_to_crawl}&page={page_number}'
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

def custom_filter(words, filtering_words):
    return [word for word in words if all(word not in censor for censor in filtering_words)]

def preprocess_data(text):
    koreanFiltered = re.findall(r'\b[가-힣]{2,15}\b', text) #string to array
    filteredKoreanWords = custom_filter(koreanFiltered, FILTERING_WORDS)

    return filteredKoreanWords

def word_cloud(frequency_dictionary):
    wc = WordCloud(font_path=FONT_PATH, max_words=MAX_WORDS, background_color=BACKGROUND_COLOR, width=WIDTH_SIZE, height=HEIGHT_SIZE)
    plt.imshow(wc.generate_from_frequencies(frequency_dictionary), interpolation='bilinear')
    plt.axis("off")
    plt.show()

    return

def custom_word_count(words):
    d = defaultdict(dict)
    for word in words:
        case_dict = d[word] # retrieve or initialize
        case_dict[word] = case_dict.get(word, 0) + 1 # increment frequency

    fused_cases = {}
    item1 = itemgetter(1)
    for key_word, case_dict in d.items():
        # Get the most popular case.
        first = max(case_dict.items(), key=item1)[0]
        fused_cases[first] = sum(case_dict.values())

    return fused_cases

def main():
     # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Crawl pages and generate a word cloud.')

    # Add the -date or -d argument
    parser.add_argument('-date', '-d', help='Date in YYYYMMDD format', required=True)

    # Parse the command-line arguments
    args = parser.parse_args()

    # Extract the date argument
    date_to_crawl = args.date
    # max_page_number = get_last_page_number()

    crawled_data_in_string = crawling_parallel(date_to_crawl)

    korean_words = preprocess_data(crawled_data_in_string)

    # word count into dictionary
    frequency_dictionary = custom_word_count(korean_words)

    # draw wordcloud
    word_cloud(frequency_dictionary)

if __name__ == "__main__":
    main()
