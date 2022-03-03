from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
remove_kb = ReplyKeyboardRemove()
shit_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)


b = KeyboardButton('Заглушка ххх')
b1 = KeyboardButton('Привет🖐')
b2 = KeyboardButton('Как дела?👻')
b3 = KeyboardButton('Что ты умеешь?')
b4 = KeyboardButton('Расскажи шутку')
b5 = KeyboardButton('Брось кубик')
b6 = KeyboardButton('Хорошо😉')
b7 = KeyboardButton('Плохо😫')
b8 = KeyboardButton('Расскажи плохую шутку 🥵🤬')
b9 = KeyboardButton('Расскажи хорошую шутку 😇🤤')

def begim():
	greet_kb.add(buttons.b1, buttons.b2)