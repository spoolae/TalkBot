import python_config
import random

proposition = ""

def write_to_log(text):
	open('log.txt','a').write(str(text)+"\n")

def choose_content(text):
	if "фильм" in text.lower():
		return python_config.films
	if "аниме" in text.lower():
		return python_config.anime
	if "книгу" in text.lower():
		return python_config.books
	if "сериал" in text.lower():
		return python_config.serial
	else: 
	 	return python_config.proposition

def choose_content_proposition(text):
	if "фильм" in text.lower():
		return python_config.films_proposition
	if "аниме" in text.lower():
		return python_config.anime_proposition
	if "книгу" in text.lower():
		return python_config.books_proposition
	if "сериал" in text.lower():
		return python_config.serial_proposition
	else: 
	   	return python_config.post_proposition

def get_proposition(msg):
	global proposition
	proposition = random.choice(choose_content(msg))
	return proposition

def handler_propos(text):
	if "фильм" in text.lower() or "аниме" in text.lower() or "книгу" in text.lower() or "сериал" in text.lower():
		return False
	else:
		return True	
