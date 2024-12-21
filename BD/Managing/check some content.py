import psycopg2

# Параметры подключения к базе данных
host = "localhost"  # Или IP-адрес контейнера
port = 5432  # Порт PostgreSQL
database = "mydatabase"  # Название вашей базы данных
user = "myuser"  # Имя пользователя
password = "mypassword"  # Пароль пользователя

# Подключение и выполнение запроса
try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    cursor = connection.cursor()

    # SQL-запрос для получения записей с тегом "технического характера"
    query = """
        SELECT f.feedback_id, f.feedback_text, f.rating, f.created_at, 
               ARRAY_AGG(t.tag_name) AS tags
        FROM feedbacks f
        JOIN feedback_tags ft ON f.feedback_id = ft.feedback_id
        JOIN tags t ON ft.tag_id = t.tag_id
        WHERE EXISTS (
            SELECT 1
            FROM feedback_tags ft_sub
            JOIN tags t_sub ON ft_sub.tag_id = t_sub.tag_id
            WHERE ft_sub.feedback_id = f.feedback_id AND t_sub.tag_name = 'технический'
        )
        GROUP BY f.feedback_id;
        """

    cursor.execute(query)
    results = cursor.fetchall()

    for record in results:
        print(record)

except Exception as e:
    print(f"Error: {e}")
finally:
    if connection:
        cursor.close()
        connection.close()
