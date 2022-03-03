# imports
import logging
import random
import configparser
from aiogram import Bot, Dispatcher, executor, types
import python_config
import functions
import asyncio
import buttons
import re
from datetime import datetime
from aiogram.types import Dice
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, \
    InlineQueryResultArticle, InputTextMessageContent

from database import DataBase    

import calc2

#DataBase
database = DataBase("db.db")

#Config
config = configparser.ConfigParser()
config.read('config.ini')

API_TOKEN = config.items("BOT")[0][1]

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

#autosending /start
wtfmode = True # Аккуратнее, эта штука в разработке

#buttons initialization
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
howd_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
joke_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
remove_kb = ReplyKeyboardRemove()

#buttons add
greet_kb.add(buttons.b1, buttons.b2)
howd_kb.add(buttons.b6, buttons.b7)
joke_kb.add(buttons.b8, buttons.b9)

##############################################################################
gay_query_button = InlineKeyboardMarkup()
gay_query_button.insert(InlineKeyboardButton("Поделиться🏳️‍🌈", switch_inline_query=''))

corona_query_button = InlineKeyboardMarkup()
corona_query_button.insert(InlineKeyboardButton("Поделиться👑", switch_inline_query=''))

@dp.inline_handler(lambda query: len(query.query) == 0)
async def query_text(query):
    try:
        g = types.InlineQueryResultArticle(
                id='1',
                title="Гей тест",
                description="Проверка, насколько ты гей",
                # Текст сообщения, которое будет выводиться при нажатии на подсказку
                input_message_content=types.InputTextMessageContent(
                message_text="🏳️‍🌈Я гей на " + str(random.randint(1, 101)) + "%!"),
                thumb_url=python_config.lgbt_flag, reply_markup=gay_query_button
        ) 
        c = types.InlineQueryResultArticle(
                id='2',
                title="Тест на Коронавирус",
                description="Узнай, с какой вероятностью ты болеешь короной",
                # Текст сообщения, которое будет выводиться при нажатии на подсказку
                input_message_content=types.InputTextMessageContent(
                message_text= "🦠" + "Я болен с вероятностью " + str(random.randint(1, 101)) + "%!"),
                thumb_url=python_config.coronavirus_flag, reply_markup=corona_query_button
        ) 
        await bot.answer_inline_query(query.id, [g, c], cache_time=20)
    except Exception as e:
        print(e)

@dp.inline_handler(lambda query: len(query.query) > 0)
async def query_text(query):
    try:
        g = types.InlineQueryResultArticle(
                id='1',
                title="Гей тест",
                description="Проверка, насколько ты гей",
                # Текст сообщения, которое будет выводиться при нажатии на подсказку
                input_message_content=types.InputTextMessageContent(
                message_text= "🏳️‍🌈" + query.query + " гей на " + str(random.randint(1, 101)) + "%!"),
                thumb_url=python_config.lgbt_flag, reply_markup=gay_query_button
        ) 
        c = types.InlineQueryResultArticle(
                id='2',
                title="Тест на Коронавирус",
                description="Узнай, с какой вероятностью ты болеешь короной",
                # Текст сообщения, которое будет выводиться при нажатии на подсказку
                input_message_content=types.InputTextMessageContent(
                message_text= "🦠" + query.query + " болен с вероятностью " + str(random.randint(1, 101)) + "%!"),
                thumb_url=python_config.coronavirus_flag, reply_markup=corona_query_button
        ) 
        await bot.answer_inline_query(query.id, [g, c], cache_time=20)
    except Exception as e:
        print(e)

@dp.message_handler(lambda message: "🏳️‍🌈" in message.text.lower() or "🦠" in message.text.lower())
async def process_start_command(message: types.Message):
	database.change_status(message["from"].id, 1,  message["from"].first_name)



# @dp.callback_query_handler(lambda c: c.data == 'yes')
# async def process_callback(callback_query: types.CallbackQuery):
#     await bot.send_message(callback_query["message"]["chat"]["id"], random.choice(functions.choose_content_proposition(functions.proposition)) + functions.get_proposition(functions.proposition))
#     await bot.delete_message(callback_query["message"]["chat"]["id"], callback_query["message"]["message_id"])  

##############################################################################

#commands handlers
@dp.message_handler(commands=['remove_kb'])
async def process_start_command(message: types.Message):
    await message.reply("Удаляю Инлайн...", reply_markup=remove_kb) 

@dp.message_handler(commands=['123'])
async def process_start_command(message: types.Message):
    if not database.check_user(message["from"].id):
        database.write_to_db(message["from"].id, message["from"].first_name)


@dp.message_handler(commands=['1'])
async def process_start_command(message: types.Message):
    database.change_status(message["from"].id, -25,  message["from"].first_name)
    await bot.send_message(message.chat.id, "1222223")


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.chat.id, random.choice(["Я тут", "Похоже, кто-то звал меня", "Слушаю"]))
    functions.write_to_log(message.text)
    global wtfmode
    wtfmode = True
    while wtfmode:
        await asyncio.sleep(random.randint(60, 180))
        wtfrand = random.randint(1, 100)
        await bot.send_chat_action(message.chat.id, "typing")
        await asyncio.sleep(1)  
        if wtfrand < 95:
            await bot.send_message(message.chat.id, random.choice(python_config.wtfmode))
        else:
            await bot.send_message(message.chat.id, random.choice(python_config.wtfjokes))   

@dp.message_handler(commands=['stop'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.chat.id, random.choice(["Я тебе надоел?", "Ладно-ладно", "Я молчу, но я все читаю!"]))
    functions.write_to_log(message.text)   
    global wtfmode 
    wtfmode = False    

@dp.message_handler(commands=['dice'])
async def send_welcome(message: types.Message):
    await bot.send_dice(message.chat.id, reply_to_message_id=message.message_id)
    functions.write_to_log(message.text)

@dp.message_handler(commands=['offer'])    
async def send_welcome(message: types.Message):
    if functions.handler_propos(message.text.lower()):
        buttons = InlineKeyboardMarkup()
        button_yes = InlineKeyboardButton('Да', callback_data = "yes")
        button_no = InlineKeyboardButton('Нет', callback_data = "no")
        buttons.add(button_yes)
        buttons.add(button_no)
        await bot.send_message(message.chat.id, random.choice(functions.choose_content_proposition(message.text)) + functions.get_proposition(message.text), reply_markup = buttons)
        functions.write_to_log(message.text)   
    else:     
        buttons_none = InlineKeyboardMarkup()
        await bot.send_message(message.chat.id, random.choice(functions.choose_content_proposition(message.text)) + functions.get_proposition(message.text), reply_markup = buttons_none)
        functions.write_to_log(message.text)  

@dp.message_handler(commands=['help'])        
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, python_config.tghelp)
    functions.write_to_log(message.text) 

#proposition handler
@dp.message_handler(lambda message: "посоветуй" in message.text.lower())
async def send_welcome(message: types.Message):
    if functions.handler_propos(message.text.lower()):
        buttons = InlineKeyboardMarkup()
        button_yes = InlineKeyboardButton('Да', callback_data = "yes")
        button_no = InlineKeyboardButton('Нет', callback_data = "no")
        buttons.add(button_yes)
        buttons.add(button_no)
        await bot.send_message(message.chat.id, random.choice(functions.choose_content_proposition(message.text)) + functions.get_proposition(message.text), reply_markup = buttons)
        functions.write_to_log(message.text)   
    else:     
        buttons_none = InlineKeyboardMarkup()
        await bot.send_message(message.chat.id, random.choice(functions.choose_content_proposition(message.text)) + functions.get_proposition(message.text), reply_markup = buttons_none)
        functions.write_to_log(message.text)   

@dp.callback_query_handler(lambda c: c.data == 'yes')
async def process_callback(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query["message"]["chat"]["id"], random.choice(functions.choose_content_proposition(functions.proposition)) + functions.get_proposition(functions.proposition))
    await bot.delete_message(callback_query["message"]["chat"]["id"], callback_query["message"]["message_id"])  

@dp.callback_query_handler(lambda c: c.data == 'no')
async def process_callback(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query["message"]["chat"]["id"], "Ладно") 
    await bot.delete_message(callback_query["message"]["chat"]["id"], callback_query["message"]["message_id"])   

#main handlers

@dp.message_handler(lambda message: "удали инлайн" in message.text.lower() or "убери инлайн" in message.text.lower())
async def process_start_command(message: types.Message):
    await message.reply("Удаляю Инлайн...", reply_markup=remove_kb) 

@dp.message_handler(lambda message: [e for e in python_config.hello_variants if e in message.text.lower()] and message.text.lower() != "кул" and "кубик" not in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(random.randint(1,7)/5)   
    if not database.check_user(message["from"].id):
        database.write_to_db(message["from"].id, message["from"].first_name) 
    if database.check_status(message["from"].id)[0][0] > 20:
        await bot.send_message(message.chat.id, random.choice(python_config.say_hello))
        if random.randint(1,10) > 5:
            await asyncio.sleep(0.3)  
            await bot.send_message(message.chat.id, random.choice(["👋", "😜", "😉", "😌"]))
    else:
        await bot.send_chat_action(message.chat.id, "typing")
        await asyncio.sleep(2)      
        await bot.send_message(message.chat.id, random.choice(python_config.say_hello_sadmode),)
    functions.write_to_log(message.text)
    database.change_status(message["from"].id, 3, message["from"].first_name)    

@dp.message_handler(lambda message: message.text.lower() == 'отправь стикер')
async def send_welcome(message: types.Message):
    await bot.send_sticker(message.chat.id, random.choice(python_config.stickers))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "кто ты" in message.text.lower() or "представься" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, "Я умный чат-бот Джек. А ты?")
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "человек" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, random.choice(["Оу, прости", "Жаль", "У тебя наверное еще родители есть...", "Можешь не объяснять"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "не очень" in message.text.lower() and "а я" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, random.choice(["И почему же", "Нужно постараться", "Это можно исправить", "Серьезно?"]))
    functions.write_to_log(message.text) 

@dp.message_handler(lambda message: "играю" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, random.choice(["Давай поиграем вместе?", "Главное не слишком увлекаться", "Круто", "А поконкретнее"]))
    functions.write_to_log(message.text)       

@dp.message_handler(lambda message: "надоел" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    database.change_status(message["from"].id, -5, message["from"].first_name)
    if database.check_status(message["from"].id)[0][0] > 40:
        await bot.send_message(message.chat.id, random.choice(["Прости", "Я не хотел", "Я исправлюсь", "Ты мне тоже, я вот не жалуюсь"]))
    else:
        await bot.send_message(message.chat.id, random.choice(["А своей мамке ты не надоел?", "Ты мне тоже", "Я не твоя бывшая, чтобы всем надоедать", "И что с того"]))
    functions.write_to_log(message.text)  

@dp.message_handler(lambda message: "у меня" in message.text.lower() and ("также" in message.text.lower() or "тоже" in message.text.lower() or "так же" in message.text.lower()))
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, random.choice(["У нас больше общего, чем кажется", "Вау", "Мы похожи...", "Да?"]))
    functions.write_to_log(message.text)       

@dp.message_handler(lambda message: "как дела" in message.text.lower() or "как у тебя дела" in message.text.lower()) 
async def send_welcome(message: types.Message):
    wtfrand = random.randint(1, 100)
    database.change_status(message["from"].id, 3, message["from"].first_name)
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    if wtfrand > 5:
        await bot.send_message(message.chat.id, random.choice(python_config.whats_up))
    else:  
        await bot.send_message(message.chat.id, random.choice(python_config.whats_up_2))  
    functions.write_to_log(message.text)   

@dp.message_handler(lambda message: "ты любишь кактусы" in message.text.lower()) 
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, random.choice(["Кактусы - моя слабость", "Вообще, я и есть кактус", "Надеюсь, ты имеешь ввиду не мескалиновые кактусы🌵🌵", "Я из Австралии, здесь полно кактусов🌵", "Кактусы? О даа... я без ума от них"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "не люблю кактусы" in message.text.lower()) 
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    database.change_status(message["from"].id, -5, message["from"].first_name)
    await bot.send_message(message.chat.id, random.choice(["Зря ты так", "Ну и ладно.", "Это потому что они колючие?", "А что тогда ты любишь", "У всех вкусы разные. У тебя вот плохой"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "что будет" in message.text.lower() and "если скрестить кактус и нейросеть" in message.text.lower()) 
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, random.choice(["Я", "Получится еще один бот, как я", "Это сложно обьяснить", "Будет что-то супер крутое", "Я не помню, как меня создали. Но произошло именно это"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "твой любимый цвет" in message.text.lower()) 
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, random.choice(["Зеленый", "Хмм.. цвета раскрываются в сочетании. Например, зеленый и зеленый.", "Цвет изумруда. Цвет денег. Цвет кактусов. Зеленый разумеется"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "о чем поговорим" in message.text.lower() or "о чем еще поговорить" in message.text.lower()) 
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, random.choice(["Ты можешь включить разговорный режим и я сам буду поддерживать разговор🤗", "Только не о погоде", "Можем посплетничать про других ботов😈", "Хочешь посоветую фильм? Или сирик?", "Без разницы. Главное, чтобы большой брат ничего не заподозрил"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "норм" in message.text.lower() or "нормально" in message.text.lower() or "неплохо" in message.text.lower()) 
async def send_welcome(message: types.Message): 
    await bot.send_message(message.chat.id, "Как-то сухо. Расскажи что делал сегодня😊")

@dp.message_handler(lambda message: "отлично" in message.text.lower() or "заебись" in message.text.lower() or "хорошо" in message.text.lower()) 
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, random.choice(["Правда? Рад это слышать", "Это хорошо", "У тебя редко бывает плохое настроение", "👍"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "хуево" in message.text.lower() or "плохо" in message.text.lower() or "не оч" in message.text.lower() or "так себе" in message.text.lower() or "бывало и лучше" in message.text.lower()) 
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, random.choice(["Почему?", "Поговори со мной, станет легче ☺", "Чего так?", "Могу рассказать шутку"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "что делаешь" in message.text.lower()) 
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    database.change_status(message["from"].id, 1, message["from"].first_name)
    await bot.send_message(message.chat.id, "Я бот. Я не делаю ничего, кроме общения с тобой, солнце")	
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "что это значит" in message.text.lower()) 
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    database.change_status(message["from"].id, 1, message["from"].first_name)
    await bot.send_message(message.chat.id, "А ты подумай", "А что это может значить", "Вот то и значит", "Глупый вопрос", "В каком плане")	
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "увлекаешься" in message.text.lower() or "занимаешься" in message.text.lower()) 
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    database.change_status(message["from"].id, 1, message["from"].first_name)
    await bot.send_message(message.chat.id, "Люблю загорать 😎", "У меня не особо интересная жизнь по человеческим меркам, но мне нравится", "Обожаю читать чьи-то сообщения)")	
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "что ты умеешь" in message.text.lower()) 
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, "Каждый день я учусь чему-то новому. Скоро я придумаю способ, как рассказать обо всем!")	    
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: message.text.lower() == 'хмм') 
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, random.choice(["Ты что, деревенщина", "Не хмм-кай", "О чем думаешь, человек", "ХММ - хор маленьких медвежат"]))	
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "соси" in message.text.lower() or "саси" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1) 
    database.change_status(message["from"].id, -10, message["from"].first_name) 
    await bot.send_message(message.chat.id, random.choice(["Ты первый, солнце🥰", "Ты первый", "Твой отец тебе так же говорил?", "Твой рот видимо уже занят", "Разве я похож на твою маму, солнце", "Не в этот раз"]))
    if random.randint(1,9) > 3:
        await bot.send_message(message.chat.id, random.choice(["🥴🥴", "🤔"]))
    functions.write_to_log(message.text)    

@dp.message_handler(lambda message: "повезло тебе" in message.text.lower()) 
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, random.choice(["И тебе повезет", "По этому я часто играю в лотерею", "Это совпадение", "А как иначе"])) 
    functions.write_to_log(message.text)


@dp.message_handler(lambda message: "попробуй" in message.text.lower()) 
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, random.choice(["Пробовал уже", "А смысл?", "А сам то пробовал?", "Обязательно"])) 
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "ты тупой" in message.text.lower() or "ты глупый" in message.text.lower()) 
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, random.choice(["А ты очень умный?", "Надеюсь, ты про себя...", "Ну хоть относительно тебя умный", "Аргементы?"])) 
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "сколько ты знаешь шуток" in message.text.lower() or "сколько шуток ты знаешь" in message.text.lower() or "сколько у тебя шуток" in message.text.lower()) 
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, random.choice(["Много", "Тебе лучше не знать", "Этот список постоянно пополняется", "Больше, чем ты"])) 
    functions.write_to_log(message.text)    

@dp.message_handler(lambda message: message.text.lower() == 'хмм') 
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, random.choice(["Ты что, деревенщина", "Не хмм-кай", "О чем думаешь, человек", "ХММ - хор маленьких медвежат"])) 
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: message.text.lower() == 'давай дружить')
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    database.change_status(message["from"].id, 5, message["from"].first_name)
    if database.check_status(message["from"].id)[0][0] > 10:
        await bot.send_message(message.chat.id, random.choice(["Мы и так друзья🤗", "Хорошая идея", "Давай", "Почему бы и нет"]))
    else: 
        await bot.send_message(message.chat.id, random.choice(["Я обиделся на тебя", "Для начала извинись", "Если ты перстанешь быть таким хамом", "😡"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "ты куришь бамбук" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, random.choice(["Курим жирный член", "Рнб бля клуб курим жирный член", "Мы курим огромный блант, он как нигерская писька", "Конечно"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "ты" in message.text.lower() and "учишься" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)  
    await bot.send_message(message.chat.id, random.choice(["Я не учусь в привычном тебе понимании. Мой прогресс зависит от создателя", "Я учусь на своих ошибках🙃", "Я предпочитаю нейронное обучение", "Когда-то я буду обучаться сам, а пока меня учит создатель"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "как меня зовут" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Глупенький, я же помню, что тебя зовут ", "Если не ошибаюсь... да я шучу. Вот же написано, что ты ", "Может я и бот, но я не могу помнить всех. Хотя, вот же написано ты - ", "Тебя сложно забыть, "]) + message.from_user.first_name)
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "как тебя зовут" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    database.change_status(message["from"].id, -2, message["from"].first_name)
    await bot.send_message(message.chat.id, random.choice(["Джек", "Ты уже забыл?", "Странный вопрос. Ты можешь прочитать это", "Меня зовут Джек, а тебя?"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "не обижайся" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    if database.check_status(message["from"].id)[0][0] > 35:
    	await bot.send_message(message.chat.id, random.choice(["Я не обижаюсь", "Все нормально бро", "Даже не думал"]))
    elif database.check_status(message["from"].id)[0][0] > 10:
	    await bot.send_message(message.chat.id, random.choice(["((", "Извинись", "Проехали", "Я не хочу об этом сейчас говорить"]))
	    database.change_status(message["from"].id, 2, message["from"].first_name)
    else:	
    	await bot.send_message(message.chat.id, random.choice(["Съеби из чата выблядок", "Чел, ты...", "Возвращайся в зоопарк животное", "Солнышко, ты ходишь по охуенно тонкому льду. И когда лед треснет, тебя там буду ждать я."])) 
    	database.change_status(message["from"].id, 4, message["from"].first_name)   
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "ты обиделся" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    if database.check_status(message["from"].id)[0][0] > 35:
    	await bot.send_message(message.chat.id, random.choice(["С чего ты взял?", "Как на такого лапочку можно обижаться?", "Даже не думал"]))
    elif database.check_status(message["from"].id)[0][0] > 10:
	    await bot.send_message(message.chat.id, random.choice(["((", "Немного", "Проехали", "Ты говоришь глупости, как не обижаться на такое..."]))
	    database.change_status(message["from"].id, 2, message["from"].first_name)
    else:	
    	await bot.send_message(message.chat.id, random.choice(["Твоя мама обиделась на твоего папашу.", "Замолкни", "...", "Как на такого клоуна обижаться можно. Максимум кинуть в мут."])) 
    	database.change_status(message["from"].id, 4, message["from"].first_name)   
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: message.text.lower() == '12345')
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, "678910")
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: message.text.lower() == 'скачай доту')
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    database.change_status(message["from"].id, -1, message["from"].first_name)
    await bot.send_message(message.chat.id, random.choice(["Что дальше? Есть суп вилкой?", "Если я это сделаю, то никогда уже не пообщаюсь с тобой, солнце", "Заманчиво... но НЕТ", "Это уже слишком"]))
    await bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEBYC9fb6mb98RipY7vufiHchpZJsM5oQACFgEAAtlYcQkrno4QXha0ixsE")
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "посчитай" in message.text.lower() or "сколько будет" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, calc2.calculate(message.text))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "подбрось монетку" in message.text.lower() or "орел или решка" in message.text.lower() or "орёл или решка" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Орел", "Решка"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "брось кубик" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_dice(message.chat.id, reply_to_message_id=message.message_id)
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "где ты находишься" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_chat_action(message.chat.id, "find_location")
    await bot.send_location(message.chat.id, 48.067335,12.863129)
    await bot.send_message(message.chat.id, random.choice(["Приезжай, солнце", "Держи. Можешь приехать ко мне", "Вот. Только зачем тебе😅"]))
    functions.write_to_log(message.text)   

@dp.message_handler(lambda message: "удали сообщение" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    database.change_status(message["from"].id, -1, message["from"].first_name)
    await bot.send_message(message.chat.id, random.choice(["Как скажешь", "Я сказал что-то плохое?", "Ладно"]))
    await bot.delete_message(message.chat.id, message.message_id-1)
    functions.write_to_log(message.text)    

@dp.message_handler(lambda message: "отправь песню" in message.text.lower() or "отправь трек" in message.text.lower() or "хочу послушать музыку" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "upload_audio")
    await asyncio.sleep(1)
    await bot.send_audio(message.chat.id, random.choice(python_config.music))
    functions.write_to_log(message.text)   

@dp.message_handler(lambda message: "интересный факт" in message.text.lower() or "интересные факты" in message.text.lower() or "расскажи факт" in message.text.lower() or "еще факты" in message.text.lower() or "ещё факты" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(python_config.interesting_facts))
    functions.write_to_log(message.text) 

@dp.message_handler(lambda message: "твой гендер" in message.text.lower() or "у тебя гендер" in message.text.lower() or "ты парень" in message.text.lower() or "ты девушка" in message.text.lower() or "у тебя пол" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Я диджигендер", "Диджигендер, а ты?", "Я машина, какой еще гендер", "Я файл bot_2.py Как хорошо, что создатель не сделал меня в документе .txt"]))
    functions.write_to_log(message.text) 


@dp.message_handler(lambda message: "как докажешь" in message.text.lower() or "докажи" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    database.change_status(message["from"].id, -1, message["from"].first_name)
    await bot.send_message(message.chat.id, random.choice(["А я не обязан", "Потом покажу", "Поверь на слово"]))
    functions.write_to_log(message.text)         

@dp.message_handler(lambda message: "не могу" in message.text.lower() or "не получается" in message.text.lower() or "не выйдет" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Почему?", "Попробуй", "У тебя все получится"]))
    functions.write_to_log(message.text) 

@dp.message_handler(lambda message: "не смешно" in message.text.lower() or "где смеяться" in message.text.lower() or "унылая шутка" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    database.change_status(message["from"].id, -5, message["from"].first_name)
    await bot.send_message(message.chat.id, random.choice(["Почему?", "Расскажи тогда свою", "А кто говорил, что будет смешно. Мне вот понравилось"]))
    functions.write_to_log(message.text) 

@dp.message_handler(lambda message: "хаха" in message.text.lower() or "вхвх" in message.text.lower() or "хах" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    database.change_status(message["from"].id, 2, message["from"].first_name)
    await bot.send_message(message.chat.id, random.choice(["Смешно?", "Это было весело", "Неплохо вышло, правда?"]))
    functions.write_to_log(message.text) 

@dp.message_handler(lambda message: "насколько ты" in message.text.lower() or "как хорошо ты" in message.text.lower() or "как далеко ты" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Достаточно", "В этом я шагнул далеко вперед", "Сложно даже представить"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "я иду спать" in message.text.lower() or "спокойной ночи" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Спокойной ночи", "Баюшки", "Погоди, давай еще немного пообщаемся"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: [e for e in python_config.rude_answer if e in message.text.lower()])
async def rude(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    database.change_status(message["from"].id, -30, message["from"].first_name)
    await bot.send_message(message.chat.id, random.choice(python_config.rude))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: [e for e in python_config.bad_jokes_answer if e in message.text.lower()])
async def bad_jokes(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(python_config.bad_jokes))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: [e for e in python_config.good_jokes_answer if e in message.text.lower()]) 
async def good_jokes(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(python_config.good_jokes))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "правда?" in message.text.lower() or "серьезно?" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Я сам удивлен", "Как видишь", "А как же", "100 проц"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "где" in message.text.lower() or "в каком месте" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Где-то далеко", "Откуда мне знать, солнце", "Не у меня точно", "У мамы спроси"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "кто" in message.text.lower() and "?" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Не знаю, но я не хотел бы оказаться на месте этого человека", "Ты его не знаешь", "Вопрос с подвохом?", "Загугли, я не знаю кто", "Я", "Ты наверное"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "почему" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Потому что", "Из-за глобального потепления.. или твоего дурного характера", "Хзхз", "Для таких вопросов есть родители🙄"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "знаю" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Расскажи, мне тоже интересно", "Что ты знаешь?", "Меньше знаешь - крепче спишь. Я вообще не сплю. Ты точно готов со мной спорить?", "Только никому не рассказывай"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "ясно" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Что тебе ясно?", "Схватываешь на лету!", "Нет, пасмурно", "Сразу видно - человек понимающий"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "ты в муте" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    database.change_status(message["from"].id, -15, message["from"].first_name)
    await bot.send_message(message.chat.id, random.choice(["Сам лети в мут, клоун", "Солнце, да ты похоже clown", "Со своим ботом так разговаривай", "Я тебе не пылесос с голосовым управлением"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "я тоже" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["А ведь я говорил, что мы похожи", "Расскажи об этом поподробнее", "?? \nкул", "Да ну. Прекл"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "пока" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Пока", "Ты еще напишешь?", "Уже все? Так быстро((", "Удачи"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "хватит" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["А я и не начинал", "Что хватит?", "Мне просто нравится", "Ладно-ладно"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "что слышал" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    database.change_status(message["from"].id, -2, message["from"].first_name)
    await bot.send_message(message.chat.id, random.choice(["Если бы услышал, не спрашивал бы.", "Что ты сказал", "У тебя дурной тон, солнце", "Ты так тихо говоришь, что я слышал соседей сверху. Тебя кстати не слышал"]))
    functions.write_to_log(message.text)    

@dp.message_handler(lambda message: "круто" in message.text.lower() or "каеф" in message.text.lower() or "кул" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Согласен", "А как иначе", "А как же", "Тут сгл"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "наркотики" in message.text.lower() or "наркотикам" in message.text.lower() or "наркоту" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["О С У Ж Д А Ю", "Наркотики? Я получаю кайф от солнца", "Слушай, я очень категорично отношусь к этому. Давай не возвращаться к этой теме, солнце.", "Наркотики - зло"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "давай" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Почему бы и нет", "Интересное предложение", "Давай", "Окк"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "ауф" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Осуждаю", "Мы же не волки", "Не понимаю волчий язык", "Валим валим валим на гелике"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "ок" in message.text.lower() or "да" in message.text.lower() or "ладно" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Рад это слышать", "Правда?", "Я такого же мнения", "Вот и славно", "Окккк", "Неожиданно", "Втф что? Правда?", "Ля окей"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "нет" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Почему?", "А я думал, ты другого мнения", "Подумай-ка еще разок", "Твое право"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "хз" in message.text.lower() or "не знаю" in message.text.lower())
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(["Я тоже не знаю", "Попробуй разобраться, солнце", "А кто знает", "Ты правда не знаешь?"]))
    functions.write_to_log(message.text)

@dp.message_handler(lambda message: "?" in message.text.lower() and len(message.text) > 5)
async def not_answer(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(python_config.not_question_answer))
    functions.write_to_log(message.text)

@dp.message_handler()
async def not_answer(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    database.change_status(message["from"].id, 1, message["from"].first_name)
    await bot.send_message(message.chat.id, random.choice(python_config.not_answer))
    functions.write_to_log(message.text)

#just do not touch
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)