import telebot, Config, Parser, os
from telebot import types

bot = telebot.TeleBot(Config.Token)

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
				Mas_History = Parser.START()
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
			bot.send_message(message.chat.id, Config.Admin)
		elif message.text == 'Что это такое?':
			bot.send_message(message.chat.id, Config.Opus)
		else:
			bot.send_message(message.chat.id, 'Я не знаю что ответить. Используйте только кнопки для взаимодействия с ботом.')
	except Exception as e:
		bot.send_message(message.chat.id, 'Произошла ошибка, попробуйте ещё раз 😢')
		print(" ")
		print(repr(e))

bot.polling(none_stop=True)
