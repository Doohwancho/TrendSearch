import os

NUMBER_OF_PAGES_TO_CRAWL = 1 # 1당 10페이지(신문기사 제목 200개) 크롤링
FILTERING_WORDS = ['동영상','기사','동영상기사','사진','포토','뉴스','오늘','내일','날씨','속보','사설']
FILE = os.path.dirname(__file__)
FONT_PATH = os.environ.get('FONT_PATH', os.path.join(FILE, 'Applegothic.ttf'))
WIDTH_SIZE = 1600
HEIGHT_SIZE = 1200
HIDE_BROWSER_WHILE_CRAWLING = True
BACKGROUND_COLOR = 'white'
MAX_WORDS = 400
