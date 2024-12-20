from langchain_ollama import OllamaLLM

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

# Укажите пути к вашим файлам
promt = "promt.txt"
input = "input.txt"

# Вызываем функцию и объединяем файлы
query = read_and_combine_files(promt, input)
#print("Запрос создан:" + "\n" + query)

# Создаем экземпляр Ollama LLM
llm = OllamaLLM(model="llama3")

response = llm.invoke(query)  # Используем `invoke` и передаем строку
print("\n" + "Ответ LLM:" + "\n")
# Печатаем результат
print(response)

