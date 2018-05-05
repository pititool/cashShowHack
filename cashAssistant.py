import pyscreenshot as ImageGrab
import pytesseract
import webbrowser
import random
import re
from unidecode import unidecode
from html.parser import HTMLParser
from PIL import Image, ImageEnhance, ImageFilter
from time import sleep
from requests import get
from bs4 import BeautifulSoup as Soup
from time import time

def run_cash_show_assistant():
	csQuestion = ImageGrab.grab(bbox=(16,168, 342, 288))
	csAnswer1 = ImageGrab.grab(bbox=(50,306,310,358))
	csAnswer2 = ImageGrab.grab(bbox=(48,376,312,427))
	csAnswer3 = ImageGrab.grab(bbox=(48,444,312,495))

	# load the example image and pre-process to reduce noise
	# and increase contrast
	def pre_process_image(img):
		img = img.filter(ImageFilter.MedianFilter())
		enhancer = ImageEnhance.Contrast(img)
		img = enhancer.enhance(2)
		img = img.convert('1')
		return img

	def convert_image_to_text(img):
		img.save('temp.jpg')
		text = pytesseract.image_to_string(Image.open('temp.jpg'))
		text = text.replace("\n", " ")
		return text

	def clean_me(html):
	    soup = Soup(html, "html.parser") # create a new bs4 object from the html data loaded
	    for script in soup(["script", "style"]): # remove all javascript and stylesheet code
	        script.extract()
	    # get text
	    text = soup.get_text()
	    # break into lines and remove leading and trailing space on each
	    lines = (line.strip() for line in text.splitlines())
	    # break multi-headlines into a line each
	    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	    # drop blank lines
	    text = '\n'.join(chunk for chunk in chunks if chunk)
	    return text

	def hash_count(html_str, answer):
		#filter out stop words in answers
		stop_words = ['the', 'a', 'an', 'is', 'are', 'to', 'from', 'in', 
		'and', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'it', 
		'its', 'of', 'on', 'that', 'to', 'was', 'were', 'will', 'with']
		counter = 0
		answer_arr = answer.split()
		answer_arr = [w for w in answer_arr if not w in stop_words]
		for word in answer_arr:
			counter = counter + html_str.count(word)
		return counter

	csQuestion = pre_process_image(csQuestion)
	question = convert_image_to_text(csQuestion)
	question = unidecode(question.split("?", 1)[0])
	print(question)

	csAnswer1 = pre_process_image(csAnswer1)
	csAnswer2 = pre_process_image(csAnswer2)
	csAnswer3 = pre_process_image(csAnswer3)
	answer1 = unidecode(convert_image_to_text(csAnswer1).strip().lower())
	answer2 = unidecode(convert_image_to_text(csAnswer2).strip().lower())
	answer3 = unidecode(convert_image_to_text(csAnswer3).strip().lower())

	print(answer1)
	print(answer2)
	print(answer3)

	# -------------- Testing -----------------

	# question = "What was used to create the communication device Liam Neeson used on screen in Star Wars: Episode 1"
	# answer1 = "women's razor"
	# answer2 = "a talking board"
	# answer3 = "a harmonica"

	# ---------------------------------------

	question = question.replace(" ", "+")
	question = question.replace("&", "%26")

	responseFromQuestion = get("https://google.com/search?q=" + question)
	h = HTMLParser()
	html = responseFromQuestion.text.lower()

	# Change HTML to punctuation encoding to actul punctuation
	html = h.unescape(html)
	html = clean_me(html)

	# Get rid of HTML tags in HTML output
	cleanr = re.compile('<.*?>')
	html = re.sub(cleanr, '', html)

	# Count instances of answer and lower-case answer
	count1 = html.count(answer1)
	count2 = html.count(answer2)
	count3 = html.count(answer3)

	# Write to file to see HTML
	# text_file = open("Output.txt", "w")
	# text_file.write(html)
	# text_file.close()

	if count1 == 0 and count2 == 0 and count3 == 0:
		print(" --------------------- ")
		print("RE-ATTEMPTING")
		count1 = hash_count(html, answer1)
		count2 = hash_count(html, answer2)
		count3 = hash_count(html, answer3)

	print(count1)
	print(count2)
	print(count3)

	if question.find("+not+") != -1 or question.find("+NOT+") != -1:
		minCount = min(count1, count2, count3)
		if minCount == count1:
			print("Answer is: 1 - " + answer1)
		if minCount == count2:
			print("Answer is: 2 - " + answer2)
		if minCount == count3:
			print("Answer is: 3 - " + answer3)
	else:
		maxCount = max(count1, count2, count3)
		if maxCount == count1:
			print("Answer is: 1 - " + answer1)
		if maxCount == count2:
			print("Answer is: 2 - " + answer2)
		if maxCount == count3:
			print("Answer is: 3 - " + answer3)

run_cash_show_assistant()
