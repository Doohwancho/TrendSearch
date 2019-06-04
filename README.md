# TrendSearch

컴퓨터를 키면 실시간 가장 핫한 키워드를 자동으로 시각화 해주는 프로그램

###########################################################################################

**사용전 세팅**

1. chrome driver 다운로드 & 설정
    크롬 드라이버 다운로드시, 크롬 버전과 맞는 것을 다운받아야 한다. 또한 driver = webdriver.Chrome("**NEED PATH**"")에서 chrome driver의 위치     를 설정해 주어야 한다.

2. 애플고딕체 다운로드 & path 설정
    시각화를 WordCloud API를 통해서 하는데, 외국에서 만든 API이다보니, 보통 한국 글씨체는 에러난다. 따라서 첨부된 AppleGothic.ttf을 
    윈도우10 기준, C:\Windows\Fonts 안에 넣어야 WordCloud가 돌아간다.
   
3. 부팅시 자동 시작 설정
    첨부파일 중 trendSearchAutoStart.bat파일이 있다. 우클릭-편집 후, trendCloud.py의 path를 입력해 준다. 다음,
    window+R 키를 누르고 실행창에서 shell:startup를 치면 시작프로그램 파일에 들어가게 된다. 이 곳에 첨부된 trendSearchAutoStart.bat을 넣어준다.


###########################################################################################

A. 프로젝트 개요 & 소개

    실시간으로 가장 트렌디한 키워드 도출 및 시각화. 각종 언론사에서 실시간으로 올라오는 기사의 정보를 가져와서, 가장 많이 언급된 단어 도출 

B. 기존 유사프로그램과의 차별성

    네이버 검색어 차트의 경우 순위 조작의 가능성 때문에 신뢰도가 적음
    미디어가 일방적으로 보여주는 정보를 사용자가 수동적으로 받아들이는 것이 아니라, 사용자가 실시간으로 가장 트렌디한 키워드를 엑티브하게 찾음 

C. 개발배경 & 필요성

    1. 대형언론사가 제공하는 정보에 대한 신뢰도가 낮아짐(ex.국정원 댓글조작사건,etc)
    2. 중요한 이슈들이 비교적 덜 중요한 이슈(ex. 연예계 이슈,etc)들 때문에 의도적으로 묻히는 경우 발생
    3. 사람들이 관심을 갖는 1차원적인 이슈와 기자들이 다루는 중요한 사회문제와의 괴리

D. 사용한 모듈 & API

    1. Crawling : Selenium과 BeautifulSoup을 사용하여 웹에 있는 정보를 가져오는 기술
    2. 정규표현식 : 가져온 정보들 중, 필요한 정보만 필터링 해주는 기술
    3. WorldCloud : 단어의 빈도수를 기준으로 시각화 해주는 API

E. 기대효과 & 활용분야

    1. 사용자는 더 이상 미디어가 대중들에게 보여주기 원하는 정보를 1차원적으로 받아들이지 않고, 현시점 가장 이슈가 되고있는 중요한 문제를 자기주적으로 찾을 수 있다. 중요한 사회문제를 정의하고 본인 나름의 시각으로 해석하는것이 가치판단능력과 Critical Thinking능력을 향상시킬 수 있다.
    2. 불필요한 가십거리 이슈보다는 진짜 사회문제에 초점을 맞출 수 있다. 
