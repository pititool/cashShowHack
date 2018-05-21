import pyscreenshot as ImageGrab
import pytesseract
import webbrowser
import random
import re
from unidecode import unidecode
from HTMLParser import HTMLParser
from PIL import Image, ImageEnhance, ImageFilter
from time import sleep, time
from requests import get
from bs4 import BeautifulSoup as Soup
from cashAssistant import run_cash_show_assistant

while 1:
	print("Appuyer sur une touche quand la question apparait")
	e = raw_input() #Attente
	print e         #Reprise
	if __name__ == '__main__':
		run_cash_show_assistant()
	sleep(2)
	continue
	
	"""csQuestion = ImageGrab.grab(bbox=(16,168, 342, 288))
	color = csQuestion.getpixel((20,20))
	if color == (255, 254, 255, 255):
		run_cash_show_assistant()
		sleep(10)"""