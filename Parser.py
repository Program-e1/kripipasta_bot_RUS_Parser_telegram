import requests, random
from bs4 import BeautifulSoup

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_URL(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('a', rel="nofollow")
	DAN = ['https://kripipasta.com' + item.get('href') for item in items if 'story' in item.get('href') and not('#' in item.get('href'))]
	return DAN

def get_content(URL_content):
	html_content = get_html(URL_content)
	html_text = BeautifulSoup(html_content.text, 'html.parser')
	OBR = html_text.find('meta', itemprop="wordCount")
	TEXT = [str(INF).strip()  for INF in OBR if not(str(INF).strip() == '<br/>' or str(INF).strip() == '')]
	for index in range(TEXT.index('<script async="" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>'), len(TEXT)-1):	TEXT.pop(index)
	TEXT.pop()

	Name = html_text.find('h1', itemprop="name")
	
	return (' '.join(TEXT), str(Name).replace('<h1 itemprop="name">', '').replace('</h1>', ''))

def  START():
	URL = 'https://kripipasta.com/story/page{0}.html'.format(str(random.randrange(1,106)))
	html = get_html(URL)
	cars = get_URL(html.text)
	return get_content(cars[random.randrange(0,len(cars))])