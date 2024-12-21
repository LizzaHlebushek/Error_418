import psycopg2
import re

host = "localhost"  # Или IP-адрес контейнера
port = 5432  # Порт PostgreSQL
database = "mydatabase"  # Название вашей базы данных
user = "myuser"  # Имя пользователя
password = "mypassword"  # Пароль пользователя

# Маппинг категорий
category_mapping = {
    "offer": "предложение",
    "claim": "жалоба",
    "gratitude": "благодарность",
    "financial": "финансы",
    "technical": "техническая часть",
    "service": "персонал"
}


# Функция для вставки отзыва и категорий в базу данных
def push_to_db(parsed_data, categories):
    print("LETS GOOOOOOO")
    print("IVE GOT THIS:" + parsed_data + categories)
    # Разделение данных отзыва
    parsed_lines = parsed_data.strip().split("\n")

    if len(parsed_lines) < 3:
        raise ValueError("Parsed data is incomplete. Expected header, date, rating, and review text.")

    # Заголовок (первое поле)
    title = parsed_lines[0].strip()

    # Дата и время (второе поле)
    date_time = parsed_lines[1].strip()

    # Оценка (третье поле)
    try:
        rating = int(parsed_lines[2].strip())
    except ValueError:
        raise ValueError("Rating must be an integer between 1 and 5.")

    # Текст отзыва (после третьего поля)
    feedback_text = "\n".join(parsed_lines[3:]).strip()

    # Соединение с базой данных
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
        VALUES (%s, %s, %s) RETURNING feedback_id
    """, (title + "\n" + feedback_text, rating, date_time))

    # Получение feedback_id вставленной записи
    feedback_id = cursor.fetchone()[0]
    print("DB GAVE ME THIS ", feedback_id)

    # Обработка категорий
    categories_list = re.split(r'[ ,]+', categories.strip())
    print("categories_list", categories_list)
    for category in categories_list:
        # Получаем название категории на русском языке из маппинга
        category_name = category_mapping.get(category.lower())
        if not category_name:
            continue

        # Вставка категории в таблицу tags (если её нет)
        cursor.execute("""
            INSERT INTO tags (tag_name)
            VALUES (%s)
            ON CONFLICT (tag_name) DO NOTHING
            RETURNING tag_id
        """, (category_name,))

        # Получение tag_id
        tag_id = cursor.fetchone()[0]

        # Связывание отзыва и категории
        cursor.execute("""
            INSERT INTO feedback_tags (feedback_id, tag_id)
            VALUES (%s, %s)
        """, (feedback_id, tag_id))

    # Подтверждение изменений и закрытие соединения
    connection.commit()
    print("I've tryed to...")
    cursor.close()
    connection.close()

