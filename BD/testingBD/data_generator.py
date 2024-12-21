import random
import string
from datetime import datetime, timedelta


# Функция для генерации случайной даты в промежутке 2023-2024
def generate_random_date():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31, 23, 59, 59)
    delta = end_date - start_date
    random_seconds = random.randint(0, int(delta.total_seconds()))
    random_date = start_date + timedelta(seconds=random_seconds)
    return random_date.strftime("%Y-%m-%d %H:%M:%S")

# Функция для генерации случайного целого числа от 1 до 5
def generate_random_number():
    return random.randint(1, 5)

# Функция для генерации случайного набора символов длиной от 300 до 4000
def generate_random_string():
    length = random.randint(30, 40)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# Функция для генерации случайного набора букв A, B, C
def generate_random_abc():
    letters = random.sample('ABC', random.randint(1, 3))  # минимально 1, максимально 3
    return ' '.join(letters)


# Функция для генерации случайного набора букв D, E, F, G
def generate_random_defg():
    letters = random.sample('DEFG', random.randint(1, 3))  # минимально 1, максимально 3
    return ' '.join(letters)





# Генерация строки
def generate_line():
    random_date = generate_random_date()
    random_string = generate_random_string()
    random_abc = generate_random_abc()
    random_defg = generate_random_defg()
    random_number = generate_random_number()

    # Формирование финальной строки
    return f"{random_date} {random_number} {random_string} {random_abc} {random_defg}"


# Пример генерации 5 строк
for _ in range(5000):
    print(generate_line())

