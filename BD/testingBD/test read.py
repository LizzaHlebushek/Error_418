import psycopg2
import pandas as pd

# Параметры подключения к базе данных
host = "localhost"  # Или IP-адрес контейнера
port = 5432  # Порт PostgreSQL
database = "mydatabase"  # Название вашей базы данных
user = "myuser"  # Имя пользователя
password = "mypassword"  # Пароль пользователя

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
    # Год и месяц, которые приходят от пользователя
    year = 2024
    month = 3

    # Запрос для извлечения записей за конкретный год и месяц
    # Запрос для извлечения записей за конкретный год и месяц с нужными столбцами
    query = """
    SELECT 
        f.rating AS opinion,         -- Рейтинг (opinion)
        t.tag_name AS category       -- Тег (category)
    FROM 
        feedbacks f
    JOIN 
        feedback_tags ft ON f.feedback_id = ft.feedback_id
    JOIN 
        tags t ON ft.tag_id = t.tag_id
    WHERE 
        EXTRACT(YEAR FROM f.created_at) = %s
        AND EXTRACT(MONTH FROM f.created_at) = %s
    ORDER BY 
        f.created_at;
    """

    # Выполнение запроса с передачей параметров
    df = pd.read_sql_query(query, connection, params=(year, month))

    # Вывод результатов
    print(df)

except Exception as e:
    print(f"Error: {e}")
finally:
    if connection:
        cursor.close()
        connection.close()




