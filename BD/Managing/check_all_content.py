import psycopg2

host = "localhost"  # Или IP-адрес контейнера
port = 5432  # Порт PostgreSQL
database = "mydatabase"  # Название вашей базы данных
user = "myuser"  # Имя пользователя
password = "mypassword"  # Пароль пользователя


# Функция для подключения и вывода всех записей
def get_all_feedbacks():
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

        # Запрос для выборки всех отзывов с их тегами
        query = """
        SELECT f.feedback_id, f.feedback_text, f.rating, f.created_at, 
               ARRAY_AGG(t.tag_name) AS tags
        FROM feedbacks f
        JOIN feedback_tags ft ON f.feedback_id = ft.feedback_id
        JOIN tags t ON ft.tag_id = t.tag_id
        GROUP BY f.feedback_id;
        """

        # Выполнение запроса
        cursor.execute(query)

        # Получаем все записи
        records = cursor.fetchall()

        # Выводим записи
        print("All Feedbacks:")
        for record in records:
            feedback_id, feedback_text, rating, created_at, tags = record
            print(f"Feedback ID: {feedback_id}")
            print(f"Text: {feedback_text}")
            print(f"Rating: {rating}")
            print(f"Created At: {created_at}")
            print(f"Tags: {', '.join(tags)}")
            print("-" * 50)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()


# Выводим все отзывы
get_all_feedbacks()