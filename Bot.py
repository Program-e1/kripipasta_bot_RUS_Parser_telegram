import telebot, os, requests, random
from bs4 import BeautifulSoup
from telebot import types

Token = '1266346072:AAHu0MZ53dIVdgAts5GRvZ3S3Rjn9LnxW4o'
Opus = "Крипипа́ста (англ. creepypasta, от англ. creepy — «жуткий» и разг. англ. copypaste — «копипаста, скопированный текст») — жанр интернет-фольклора, представляющий собой небольшие рассказы, цель которых — напугать читателя. С помощью этого бота вы сможете получить истории в формате txt файла. Для этого нажмите кнопку 'Сгенерировать историю'."
Admin = 'Есть вопрос? Или вы хотите улучшить этот сервис. Пишите ваши предложение на адрес => program.e1@mail.ru'

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

bot = telebot.TeleBot(Token)

@bot.message_handler(commands=['start'])
def welcome(message):
	
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Сгенерировать историю")
	item2 = types.KeyboardButton("Связь с разработчиком")
	item3 = types.KeyboardButton("Что это такое?")

	markup.add(item1, item2, item3)
 
	bot.send_message(message.chat.id, "Добро пожаловать.", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalala(message):
	try:
		if message.text == 'Сгенерировать историю':
			while 1:
				Mas_History = START()
				if 'часть' in Mas_History[1].lower():	continue
				else:	break

			file_new = open('{0}.txt'.format(Mas_History[1]), 'w')
			file_new.write(Mas_History[0])
			file_new.close()

			file_send = open('{0}.txt'.format(Mas_History[1]), 'rb')
			bot.send_document(message.chat.id, file_send)
			file_send.close()

			os.remove('{0}.txt'.format(Mas_History[1]))
		elif message.text == 'Связь с разработчиком':
			bot.send_message(message.chat.id, Admin)
		elif message.text == 'Что это такое?':
			bot.send_message(message.chat.id, Opus)
		else:
			bot.send_message(message.chat.id, 'Я не знаю что ответить. Используйте только кнопки для взаимодействия с ботом.')
	except Exception as e:
		bot.send_message(message.chat.id, 'Произошла ошибка, попробуйте ещё раз 😢')
		print(" ")
		print(repr(e))

bot.polling(none_stop=True)