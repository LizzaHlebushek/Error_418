import pandas as pd
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def load_data(file_path):
    try:
        return pd.read_csv(file_path, parse_dates=['date'], dayfirst=True)
    except ValueError as e:
        print("Ошибка при чтении дат:", e)
        return pd.DataFrame(columns=['date', 'text', 'category', 'opinion'])
    
    
def filter_by_year_and_month(data, year=None, month=None):
    # Преобразуем дату в формат datetime
    data['date'] = pd.to_datetime(data['date'])
    
    # Фильтруем данные по году и месяцу
    if year is not None:
        data = data[data['date'].dt.year == year]
    if month is not None:
        data = data[data['date'].dt.month == month]
    
    return data