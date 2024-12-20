from langchain_ollama import OllamaLLM
import socket

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
    return "\n".join(tmp_string)
# Укажите пути к вашим файлам
prompt_file = "prompt.txt"
with open(prompt_file, 'r', encoding='utf-8') as file:
    prompt = file.read()

# Создаем экземпляр Ollama LLM
llm = OllamaLLM(model="llama3")

HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(0)
    conn, addr = s.accept()
    data = conn.recv(4096).decode('UTF-8')
    if  data != '':
        print(data)
        tmp_string = [data.split('\n')[0]] + data.split('\n')[3:]
        query = prompt + get_message_from_data(data)
        print("Запрос создан:" + "\n" + query)
        response = llm.invoke(query)  # Используем `invoke` и передаем строку
        print("\n" + "Ответ LLM:" + "\n")
        # Печатаем результат
        print(response)
    s.close()
