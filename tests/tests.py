import unittest
import pyscreenshot as ImageGrab
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import webbrowser
import random
from time import sleep
from requests import get
from bs4 import BeautifulSoup as Soup

class TestOCR(unittest.TestCase):

    def test_cash_show_question(self):
    	img = Image.open('csQuestionSS.PNG')
        img = img.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        img = img.convert('1')
        img.save('question.jpg')
        question = pytesseract.image_to_string(Image.open('question.jpg'))
        question = question.replace("\n", " ")
        self.assertEqual(question, 'In traditional fairy tales, where do the royals live?')

    def test_cash_show_answers(self):
        img = Image.open('csAnswersSS.PNG')
        img = img.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        img = img.convert('1')
        img.save('answers.jpg')
        answers = pytesseract.image_to_string(Image.open('answers.jpg'))
        answers = answers.replace("\n", " ")
        self.assertEqual(answers, '')

    def test_hq_question(self):
        img = Image.open('hqQuestionSS.PNG')
        img = img.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        img = img.convert('1')
        img.save('question.jpg')
        question = pytesseract.image_to_string(Image.open('question.jpg'))
        question = question.replace("\n", " ")
        self.assertEqual(question, 'Bonnie 8: Clyde were wanted by police for committing what crime?')

    def test_hq_answers(self):
        img = Image.open('hqAnswerSS.PNG')
        img = img.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        img = img.convert('1')
        img.save('answers.jpg')
        answers = pytesseract.image_to_string(Image.open('answers.jpg'))
        answers = answers.replace("\n", " ")
        self.assertEqual(answers, 'Bank robbery  Excessive PDA  Destination wedding')

    def test_google_search(self):
        question = "Bonnie & Clyde were wanted by police for committing what crime?"
        answer1 = "Bank Robbery"
        answer2 = "Excessive PDA"
        answer3 = "Destination Wedding"

        question = question.replace(" ", "+")
        question = question.replace("&", "%26")
        query1 = question + " " + answer1
        query2 = question + " " + answer2
        query3 = question + " " + answer3

        response1 = get("https://google.com/search?q=" + query1)
        soup1 = Soup(response1.text, 'html.parser')
        result1 = soup1.find(id="resultStats").encode('utf-8')
        count1 = int(filter(str.isdigit, result1))
        sleep(random.uniform(0.5, 1))

        response2 = get("https://google.com/search?q=" + query2)
        soup2 = Soup(response2.text, 'html.parser')
        result2 = soup2.find(id="resultStats").encode('utf-8')
        count2 = int(filter(str.isdigit, result2))
        sleep(random.uniform(0.5, 1))

        response3 = get("https://google.com/search?q=" + query3)
        soup3 = Soup(response3.text, 'html.parser')
        result3 = soup3.find(id="resultStats").encode('utf-8')
        count3 = int(filter(str.isdigit, result3))

        maxCount = max(count1, count2, count3)
        if maxCount == count1:
            finalAnswer = answer1
        if maxCount == count2:
            finalAnswer = answer2
        if maxCount == count3:
            finalAnswer = answer3
            
        self.assertEqual(finalAnswer, "Bank Robbery")

    def find_answer_test(self):
        question = "What flower can pull radioactive contaminants from the soil"
        answer1 = "carnations"
        answer2 = "sunflowers"
        answer3 = "roses"

        question = question.replace(" ", "+")
        question = question.replace("&", "%26")

        responseFromQuestion = get("https://google.com/search?q=" + question)
        h = HTMLParser()
        html = responseFromQuestion.text.lower()

        # Change HTML to punctuation encoding to actul punctuation
        html = h.unescape(html).encode('utf-8')

        # Open website 
        # webbrowser.open("https://google.com/search?q=" + question)

        # Count instances of answer and lower-case answer
        count1 = html.count(answer1)
        count2 = html.count(answer2)
        count3 = html.count(answer3)

        if count1 == 0 and count2 == 0 and count3 == 0:
            print("Re-Attempting, first try resulted in 0s, taking first word without articles")
            answer1 = re.sub('(\s+)(a|an|and|the)(\s+)', '\1\3', answer1)
            answer2 = re.sub('(\s+)(a|an|and|the)(\s+)', '\1\3', answer2)
            answer3 = re.sub('(\s+)(a|an|and|the)(\s+)', '\1\3', answer3)
            count1 = html.count(answer1.split(" ", 1)[0])
            count2 = html.count(answer2.split(" ", 1)[0])
            count3 = html.count(answer3.split(" ", 1)[0])

        if question.find("+not+") != -1 or question.find("+NOT+") != -1:
            minCount = min(count1, count2, count3)
            if minCount == count1:
                answer = answer1
            if minCount == count2:
                answer = answer2
            if minCount == count3:
                answer = answer3
        else:
            maxCount = max(count1, count2, count3)
            if maxCount == count1:
                answer = answer1
            if maxCount == count2:
                answer = answer2
            if maxCount == count3:
                answer = answer3

        self.assertEqual(answer, answer2)

if __name__ == '__main__':
    unittest.main()