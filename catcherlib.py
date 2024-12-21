from bs4 import BeautifulSoup, Comment
import requests
from time import sleep
import socket


def printfromquotes(text, start):
    quotes1 = text[start:].find('\"')+start
    quotes2 = text[quotes1+1:].find('\"')+quotes1+1
    quotes3 = text[quotes2+1:].find('\"')+quotes2+1
    return text[quotes2+1:quotes3]

def fixformatting(text):
    text = text.replace("&lt;", "")
    text = text.replace("/ul&gt;", "")
    text = text.replace("ul&gt;", "")
    text = text.replace("/br&gt", "")
    text = text.replace("br&gt", "")
    text = text.replace("/p&gt;", "")
    text = text.replace("p&gt;", "")
    text = text.replace("/li&gt;", "")
    text = text.replace("li&gt;", "")
    text = text.replace("&quot;", '\"')
    text = text.replace(";", '\n')
    return text

def parce(url):
        data = ''
        sleep(1)
        req = requests.get(url)
        soup = str(BeautifulSoup(req.content, "html.parser"))
        start = soup.find('Review')
        soup = soup[start:]
        desc = soup.find('description')
        name = soup.find('name')
        rating = soup.find('ratingValue')
        date = soup.find('datePublished')
        file = open('parser_data.txt', "r")
        if printfromquotes(soup, date) in file.read():
            file.close()
            return data
        print('you\'ve got mail')
        file.close()
        file = open('parser_data.txt', "w")
        file.write(fixformatting(printfromquotes(soup, date)) + "\n")
        data += (fixformatting(printfromquotes(soup, name)) + "\n")
        data += (fixformatting(printfromquotes(soup, date)) + "\n")
        data += (fixformatting(printfromquotes(soup, rating)) + "\n")
        data += (fixformatting(printfromquotes(soup, desc)) + "\n")
        file.close()
        return data
