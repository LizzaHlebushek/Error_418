import psycopg2

host = "localhost"  # Или IP-адрес контейнера
port = 5432  # Порт PostgreSQL
database = "mydatabase"  # Название вашей базы данных
user = "myuser"  # Имя пользователя
password = "mypassword"  # Пароль пользователя


# Функция для получения и вывода названий таблиц и их полей
def get_tables_and_columns():
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

        # Получение списка всех таблиц в базе данных
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tables = cursor.fetchall()

        # Для каждой таблицы получаем список столбцов
        for table in tables:
            table_name = table[0]
            print(f"Table: {table_name}")

            # Получение столбцов для данной таблицы
            cursor.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = %s;
            """, (table_name,))
            columns = cursor.fetchall()

            for column in columns:
                print(f"  - {column[0]}")

            print("\n")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()


# Запуск функции
if __name__ == "__main__":
    get_tables_and_columns()