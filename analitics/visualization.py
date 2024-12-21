import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import logging


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def save_plot_to_html(plot_function, filename):
    buf = BytesIO()
    plot_function()
    plt.savefig(buf, format='png')
    plt.close()
    encoded_image = base64.b64encode(buf.getvalue()).decode('utf-8')
    with open(f'templates/{filename}', 'w') as f:
        f.write(f'<img src="data:image/png;base64,{encoded_image}" alt="{filename[:-5]}">')


def plot_opinions(data):
    logger.debug(f"Проверка данных для построения графика Opinions: {data.head()}")
    if len(data) > 0:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.countplot(x='opinion', data=data, ax=ax)
        plt.title('Распределение отзывов по мнению')
    else:
        raise ValueError("Нет данных для построения графика.")

def plot_categories(data):
    logger.debug(f"Проверка данных для построения графика Categories: {data.head()}")
    if len(data) > 0:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.countplot(x='category', hue='opinion', data=data, ax=ax)
        plt.title('Распределение отзывов по категориям')
    else:
        raise ValueError("Нет данных для построения графика.")
    