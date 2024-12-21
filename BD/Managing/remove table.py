import psycopg2

# Параметры подключения к базе данных
host = "localhost"  # Или IP-адрес контейнера
port = 5432  # Порт PostgreSQL
database = "mydatabase"  # Название вашей базы данных
user = "myuser"  # Имя пользователя
password = "mypassword"  # Пароль пользователя


# SQL-запросы для удаления таблиц
drop_feedback_tags_table = "DROP TABLE IF EXISTS feedback_tags CASCADE;"
drop_feedbacks_table = "DROP TABLE IF EXISTS feedbacks CASCADE;"
drop_tags_table = "DROP TABLE IF EXISTS tags CASCADE;"

# Функция для удаления таблиц
def drop_tables():
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

        # Удаление таблиц
        print("Dropping tables...")

        # Удаление таблицы feedback_tags
        cursor.execute(drop_feedback_tags_table)
        print("Table 'feedback_tags' dropped successfully.")

        # Удаление таблицы feedbacks
        cursor.execute(drop_feedbacks_table)
        print("Table 'feedbacks' dropped successfully.")

        # Удаление таблицы tags
        cursor.execute(drop_tags_table)
        print("Table 'tags' dropped successfully.")

        # Сохранение изменений
        connection.commit()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

# Запуск функции удаления таблиц
if __name__ == "__main__":
    drop_tables()