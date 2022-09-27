import os

CRAWLING_PAGE = 3  # 1당 10페이지(신문기사 제목 200개) 크롤링
FILE = os.path.dirname(__file__)
FONT_PATH = os.environ.get('FONT_PATH', os.path.join(FILE, 'Applegothic.ttf'))
