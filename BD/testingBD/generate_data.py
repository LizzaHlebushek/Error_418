import psycopg2
from data_generator import generate_line
from psycopg2 import sql

# Параметры подключения к базе данных
host = "localhost"  # Или IP-адрес контейнера
port = 5432  # Порт PostgreSQL
database = "mydatabase"  # Название вашей базы данных
user = "myuser"  # Имя пользователя
password = "mypassword"  # Пароль пользователя

# Функция для извлечения данных из строки и добавления записи в базу данных
def add_feedback(feedback_string):
    # Разбираем строку
    parts = feedback_string.split(' ')
    date = parts[0] + " " + parts[1]  # Дата (2023-04-14 17:28:14)
    rating = int(parts[2])  # Оценка (целое число от 1 до 5)
    feedback_text = ' '.join(parts[3:])  # Комментарий (все символы после оценки)

    # Тэги: A, B, C, D, E, F (оставляем только уникальные)
    tags = set(parts[3:])  # Тэги
    tag_names = {'A': 'жалоба', 'B': 'предложение', 'C': 'похвала',
                 'D': 'технический', 'E': 'финансовый', 'F': 'качество персонала'}
    tag_ids = []

    try:
        # Подключение к базе данных
        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        cursor = connection.cursor()

        # Вставка отзыва в таблицу feedbacks
        cursor.execute("""
        INSERT INTO feedbacks (feedback_text, rating, created_at)
        VALUES (%s, %s, %s) RETURNING feedback_id;
        """, (feedback_text, rating, date))

        # Получаем ID вставленного отзыва
        feedback_id = cursor.fetchone()[0]

        # Добавление тэгов в таблицу tags, если их там нет
        for tag in tags:
            tag_name = tag_names.get(tag)
            if tag_name:
                cursor.execute("""
                INSERT INTO tags (tag_name)
                VALUES (%s)
                ON CONFLICT (tag_name) DO NOTHING;
                """, (tag_name,))

                # Получаем ID тега
                cursor.execute("""
                SELECT tag_id FROM tags WHERE tag_name = %s;
                """, (tag_name,))
                tag_id = cursor.fetchone()[0]
                tag_ids.append(tag_id)

        # Связываем отзывы с тегами в таблице feedback_tags
        for tag_id in tag_ids:
            cursor.execute("""
            INSERT INTO feedback_tags (feedback_id, tag_id)
            VALUES (%s, %s);
            """, (feedback_id, tag_id))

        # Сохраняем изменения
        connection.commit()
        #print("Feedback added successfully.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()


for i in range(5000):
    add_feedback(generate_line())
    if i%100 == 0 :
        print(i)
