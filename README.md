
# A. Introduction
![Alt text](./sample.png?raw=true "sample_image")
<br/>
실시간 가장 핫한 키워드를 네이버 뉴스에서 크롤링 해서 wordcloud로 시각화 해주는 프로그램
<br/>
<br/>

# B. How to install and run?

```
git clone https://github.com/Doohwancho/TrendSearch
cd TrendSearch
pip3 install -r requirements.txt
python main.py (prerequisites: python 3.8)
```


<br/>

# C. Update

## ver 1.0.13
1. feat: 영어기사 제거
2. feat: crawling 도중 command 창 숨김 기능 추가
3. performance: chrome driver options
4. build: dependencies -> requirements.txt
5. refactor: depreciated code: webdriver.Chrome();
6. refactor: configuration option separated into config.py
7. refactor: relative path for AppleGothic.ttf font
8. fix: selenium >= 4.10.0 supports Service that takes care of downloading latest compatible chrome driver
9. fix: DEPRECATED - selenium 4.18.1 does not support find_element_by_css_selector()
10. fix: 10페이지 이상 크롤링 할 수 있도록 변경
11. fix: 20페이지 이후 페이지 크롤링 시, 같은 페이지를 크롤링 하던 문제 해결
12. performance: selenium + chrome deriver -> requests + parallel
13. performance: requests + parallel + preprocessing optimization


# D. Performance Optimization

mac m1, 8 core, 1000 page crawling 기준,\
**16분 21초 -> 1분 16초로 약 15분 5초 성능개선**

1. selenium + chrome driver ------------------------------ **981,850ms** (16m 21s 850ms, 44% cpu)
2. selenium + chrome driver(optimized) ----------------- 207,200ms (3m 27s 200ms, 48% cpu)
3. requests + parallel -------------------------------------- 80,450ms (1m 20s 450ms, 169% cpu)
4. requests + parallel + preprocessing optimized ------- **76,010ms** (1m 16s 10ms, 170% cpu)



# E. 시행착오

## a. selenium에서 다른 headless browser를 쓰지 않고 단순 requests + parallel로 변경

1. 크롤링 성능향상을 고민하던 중, 하나의 쓰레드가 천개의 페이지를 순차적으로 처리하는게 아니라, **'여러개의 쓰레드가 동시에 병렬로 크롤링을 하면 더 빠르지 않을까?'** 라는 생각이 들었다.
2. 그러나 chrome driver는 thread-safe하지 않았다.
	- 물론 chrome driver객체는 쓰레드 갯수만큼(8~12) 만들고 병렬처리하면 가능은 하다.
	- 하지만 driver 객체를 초기화 시키는게 리소스를 많이 잡아 먹기에 좋은 방법은 아니라 판단되었다.
3. selenium 말고 다른 크롤링 프레임워크를 찾아본 결과, pypuppeteer과 playwright를 찾게 되었는데, 결국 단순 http 요청해서 크롤링 하는 방식을 선택하게 되었다.
	- [pypuppeteer은 depreciated 되었고, github page에서 playwright를 쓰라고 나와있다.](https://github.com/pyppeteer/pyppeteer)
	- playwright를 막상 쓰려고 보니, 크롤링하려는 페이지에서 세션관리를 요구하는 것도 아니고, JS heavy한 SPA 페이지도 아닌 단순 html 페이지 인 점을 고려하여 requests 라이브러리 + Beautifulsoup4를 사용하여 크롤링 하게 되었다.



## b. thread pool 갯수 조절로 인한 성능 향상 실패

### 1. 의문증
쓰레드 여러개를 병렬로 동시에 1000개 페이지를 크롤링 할 때,\
쓰레드 갯수를 최적갯수로 지정해주면,\
latency가 더 좋아지지 않을까?

### 2. 코드

```python
with ThreadPoolExecutor(max_workers=${number_of_threads}) as executor:
	# Submit all fetch tasks and create a future-to-page mapping
	future_to_page = {executor.submit(fetch_page, page_number): page_number for page_number in range(1, max_page_number + 1)}

	...
```


### 3. 실험결과

오히려 설정을 안한 코드보다 더 느려졌다.

- before 최적화 시도: 75,632ms
- after 최적화 시도
	1. 8 threads(8 core) : 79,718ms
	2. 9 threads(8 core + 1) : 77,725ms
	3. 10 threads(8 core + 2) : 77,088ms
	4. 11 threads(8 core + 3) : 78,829ms
	5. 12 threads (8 core + 4) : 78,097ms
	6. 13 threads (8 core + 5) : 77,024ms
	7. 14 threads (8 core + 6) : 87,127ms
	8. 15 threads(8 core + 7) : 94,737ms
	9. 16 threads(8 core + 8) : 96,220ms

### 4. 느낀점

core 갯수(8) + 2가 가장 성능이 좋았으나(77,088ms),\
설정을 안건드린 것 보다 여전히 2초가 느린걸 보면,\
저 코드가 내부적으로 쓰레드 풀에 설정을 바꾸고 쓰레드 initialize 하는 등의 과정이 추가 되었기 때문인 것으로 예측된다.


## c. 전처리 optimization

### 1. 특수문자 제거하는 코드 삭제

```python
re.sub(r'\s+', ' ', arrayToString).strip().replace('\n', '').replace('\t', '')
```

부검 결과, 이 코드에서 필터링 하고자 하는 특수문자들은 바로 다음 코드인\
`re.findall(r'\b[가-힣]{2,15}\b', refinedData)`\
한글필터링 코드에서 걸러지기 때문에 삭제한다.

### 2. 불필요한 문자열 처리 부분 스킵

[wordcloud 라이브러리](https://github.com/amueller/word_cloud/blob/main/wordcloud/wordcloud.py#L558)를 뜯어보니, 문자열을 전처리해주는 코드가 다음과 같았다. 이 메서드의 전처리 기능은 아래와 같다.
1. 길이가 2개 이상인 단어만 추출
2. 인코딩을 유니코드로 설정
3. 모든 단어를 lowercase로 변경
4. 단어 끝에 's가 붙어있다면 제거
5. 숫자 제거
6. 단어 최소 길이가 설정되어 있다면 적용
7. 금지어 제거
8. word count

문제는 이 중에서 실제로 필요한 부분은 8. word count 밖에 없고, **나머지 전부는 불필요한 CPU 리소스 낭비였다.**

- ex1. 한글이라 lowercase가 없고, 맨 뒤에 's가 붙을 일도 없으며, 숫자도 이미 필터링 되어있는 상태이다.
- ex2. 무엇보다도, 금지어 제거 부분에서 **금지어 리스트를 File I/O로 가져온다는 점**에서 매우 느렸다.

따라서 이 단계를 스킵하고, word_count가 된 dictionary를 인풋으로 받는 `wc.generate_from_frequencies()`를 사용하게 되었다.


---
```python
# 스킵한 메서드
def process_text(self, text):
	"""Splits a long text into words, eliminates the stopwords.

	Parameters
	----------
	text : string
		The text to be processed.

	Returns
	-------
	words : dict (string, int)
		Word tokens with associated frequency.

	..versionchanged:: 1.2.2
		Changed return type from list of tuples to dict.

	Notes
	-----
	There are better ways to do word tokenization, but I don't want to
	include all those things.
	"""

	flags = (re.UNICODE if sys.version < '3' and type(text) is unicode  # noqa: F821
			 else 0)
	pattern = r"\w[\w']*" if self.min_word_length <= 1 else r"\w[\w']+"
	regexp = self.regexp if self.regexp is not None else pattern

	words = re.findall(regexp, text, flags)
	# remove 's
	words = [word[:-2] if word.lower().endswith("'s") else word
			 for word in words]
	# remove numbers
	if not self.include_numbers:
		words = [word for word in words if not word.isdigit()]
	# remove short words
	if self.min_word_length:
		words = [word for word in words if len(word) >= self.min_word_length]

	stopwords = set([i.lower() for i in self.stopwords])
	if self.collocations:
		word_counts = unigrams_and_bigrams(words, stopwords, self.normalize_plurals, self.collocation_threshold)
	else:
		# remove stopwords
		words = [word for word in words if word.lower() not in stopwords]
		word_counts, _ = process_tokens(words, self.normalize_plurals)

	return word_counts
```




### 3. collections.Counter() 말고 custom_word_cound() 사용

step2에서 불필요한 단계를 스킵하기 위해서 word_count를 한 후, `wc.generate_from_frequencies()` 를 쓰면 되는걸 알았다.

word_count를 하기 위해 파이썬 라이브러리인 **collections.Counter()를 사용했는데, 성능이 오히려 느려졌다.**
```
1. before collections.Counter()
	- 114.14s user 21.95s system 169% cpu 1:20.45 total
2. after collections.Counter()
	- 121.42s user 34.66s system 184% cpu 1:24.39 total
```
그래서 **Counter 클래스가 범용 목적으로 제작된거라 safety check 같은게 성능저하 시키나?** 싶어서, 기존에 wordcloud에 있던 wordcount 메서드를 적용했더니, 성능이 좋아졌다.
```
3. collections.Counter() -> wordcloud 라이브러리의 wordcount()
	- 112.33s user 24.03s system 171% cpu 1:19.41 total
```
그런데 이 wordcount 메서드에서도 영어에서 복수형 's'가 붙은 단어는 별개 처리해주는 로직이 있는데, 어짜피 한글로 전처리 했으므로 삭제처리 하니까 성능이 빨라졌다.

```
4. 기존 word counter 메서드에서 불필요한 부분을 뺀 것
	- 110.25s user 19.14s system 170% cpu 1:16.01 total
```

---
```python
# 1. 기존 word_cloud() 메서드
def process_tokens(words, normalize_plurals=True):
    """Normalize cases and remove plurals.

    Each word is represented by the most common case.
    If a word appears with an "s" on the end and without an "s" on the end,
    the version with "s" is assumed to be a plural and merged with the
    version without "s" (except if the word ends with "ss").

    Parameters
    ----------
    words : iterable of strings
        Words to count.

    normalize_plurals : bool, default=True
        Whether to try and detect plurals and remove trailing "s".

    Returns
    -------
    counts : dict from string to int
        Counts for each unique word, with cases represented by the most common
        case, and plurals removed.

    standard_forms : dict from string to string
        For each lower-case word the standard capitalization.
    """
    # words can be either a list of unigrams or bigrams
    # d is a dict of dicts.
    # Keys of d are word.lower(). Values are dicts
    # counting frequency of each capitalization
    d = defaultdict(dict)
    for word in words:
        word_lower = word.lower()
        # get dict of cases for word_lower
        case_dict = d[word_lower]
        # increase this case
        case_dict[word] = case_dict.get(word, 0) + 1
    if normalize_plurals:
        # merge plurals into the singular count (simple cases only)
        merged_plurals = {}
        for key in list(d.keys()):
            if key.endswith('s') and not key.endswith("ss"):
                key_singular = key[:-1]
                if key_singular in d:
                    dict_plural = d[key]
                    dict_singular = d[key_singular]
                    for word, count in dict_plural.items():
                        singular = word[:-1]
                        dict_singular[singular] = (
                            dict_singular.get(singular, 0) + count)
                    merged_plurals[key] = key_singular
                    del d[key]
    fused_cases = {}
    standard_cases = {}
    item1 = itemgetter(1)
    for word_lower, case_dict in d.items():
        # Get the most popular case.
        first = max(case_dict.items(), key=item1)[0]
        fused_cases[first] = sum(case_dict.values())
        standard_cases[word_lower] = first
    if normalize_plurals:
        # add plurals to fused cases:
        for plural, singular in merged_plurals.items():
            standard_cases[plural] = standard_cases[singular.lower()]
    return fused_cases, standard_cases
```


```python
# 2. 불필요한 부분 삭제한 메서드
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
```
