import pandas as pd
import logging
import psycopg2

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Параметры подключения к базе данных
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'mydatabase',
    'user': 'myuser',
    'password': 'mypassword',
}


def connect_to_db():
    """Устанавливает соединение с базой данных."""
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        raise


def load_data_opinions(year, month):
    """Загружает данные из базы данных."""
    query = """
    SELECT 
        DATE(f.created_at) AS date, 
        f.rating AS opinion
    FROM 
        feedbacks f
    WHERE 
        EXTRACT(YEAR FROM f.created_at) = %s
        AND EXTRACT(MONTH FROM f.created_at) = %s
    ORDER BY 
        f.created_at;
    """
    try:
        with connect_to_db() as connection:
            data = pd.read_sql_query(query, connection, params=(year, month))
        logger.debug(f"Загружено {len(data)} записей из базы данных.")
        return data
    except Exception as e:
        logger.error(f"Ошибка при загрузке данных из базы: {e}")
        return 0


    
def load_data_categories(year, month):
    """Загружает данные из базы данных."""
    query = query = """
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
    try:
        with connect_to_db() as connection:
            data = pd.read_sql_query(query, connection, params=(year, month))
        logger.debug(f"Загружено {len(data)} записей из базы данных.")
        return data
    except Exception as e:
        logger.error(f"Ошибка при загрузке данных из базы: {e}")
        return 0