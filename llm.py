from langchain_ollama import OllamaLLM
from bs4 import BeautifulSoup
import requests
from push_to_db import push_to_db

def read_and_combine_files(file1, file2):
    # Открываем первый файл и читаем его содержимое
    with open(file1, "r", encoding="utf-8") as f1:
        content1 = f1.read()

    # Открываем второй файл и читаем его содержимое
    with open(file2, "r", encoding="utf-8") as f2:
        content2 = f2.read()

    # Объединяем содержимое двух файлов в одну строку
    combined_content = content1 + content2
    return combined_content

def get_message_from_data(data):
    tmp_string = [data.split('\n')[0]] + data.split('\n')[3:]
    text = "\n".join(tmp_string)
    return "\n".join([line for line in text.splitlines() if line.strip()])
# Укажите пути к вашим файлам
prompt_file = "prompt.txt"
with open(prompt_file, 'r', encoding='utf-8') as file:
    prompt = file.read()

# Создаем экземпляр Ollama LLM
llm = OllamaLLM(model="llama3")

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

file = open('parser_data.txt', "w")
file.write('fch')
url = 'https://www.banki.ru/services/responses/bank/promsvyazbank/?page=1&type=all'
while True:
    data = ''
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
        continue
    file.close()
    file = open('parser_data.txt', "w")
    file.write(fixformatting(printfromquotes(soup, date)) + "\n")
    data += (fixformatting(printfromquotes(soup, name)) + "\n")
    data += (fixformatting(printfromquotes(soup, date)) + "\n")
    data += (fixformatting(printfromquotes(soup, rating)) + "\n")
    data += (fixformatting(printfromquotes(soup, desc)) + "\n")
    file.close()
    if  data != '':
        print(data)
        message = get_message_from_data(data)
        query = prompt + message
        print("Запрос создан:" + "\n" + query)
        response = llm.invoke(query)  # Используем `invoke` и передаем строку
        print("\n" + "Ответ LLM:" + "\n")
        # Печатаем результат
        print(response)
        push_to_db(data, response)




