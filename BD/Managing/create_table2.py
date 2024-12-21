import psycopg2

host = "localhost"  # Или IP-адрес контейнера
port = 5432  # Порт PostgreSQL
database = "mydatabase"  # Название вашей базы данных
user = "myuser"  # Имя пользователя
password = "mypassword"  # Пароль пользователя

# SQL-запросы для создания таблиц
create_feedbacks_table = """
CREATE TABLE IF NOT EXISTS feedbacks (
    feedback_id SERIAL PRIMARY KEY,
    feedback_text TEXT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5), 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

create_tags_table = """
CREATE TABLE IF NOT EXISTS tags (
    tag_id SERIAL PRIMARY KEY,
    tag_name VARCHAR(255) NOT NULL UNIQUE
);
"""

create_feedback_tags_table = """
CREATE TABLE IF NOT EXISTS feedback_tags (
    feedback_id INT REFERENCES feedbacks(feedback_id) ON DELETE CASCADE,
    tag_id INT REFERENCES tags(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (feedback_id, tag_id)
);
"""

# Функция для подключения и создания таблиц
def create_tables():
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

        # Создание таблиц
        print("Creating tables...")

        # Создание таблицы feedbacks
        cursor.execute(create_feedbacks_table)
        print("Table 'feedbacks' created successfully.")

        # Создание таблицы tags
        cursor.execute(create_tags_table)
        print("Table 'tags' created successfully.")

        # Создание таблицы feedback_tags
        cursor.execute(create_feedback_tags_table)
        print("Table 'feedback_tags' created successfully.")

        # Сохранение изменений
        connection.commit()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

# Запуск функции создания таблиц
if __name__ == "__main__":
    create_tables()
