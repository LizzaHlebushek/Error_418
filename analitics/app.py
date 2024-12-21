from flask import Flask, render_template, request
from visualization import save_plot_to_html, plot_opinions, plot_categories
from utils import load_data_opinions, load_data_categories
import os
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

app = Flask(__name__, template_folder='templates', static_folder='static')

# Указываем дополнительные пути для поиска шаблонов
additional_templates_dirs = [
    os.path.join(os.path.dirname(__file__), 'templates'),
]
for directory in additional_templates_dirs:
    app.jinja_loader.searchpath.append(directory)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        year = int(request.form.get('year')) if request.form.get('year') != '' else None
        month = int(request.form.get('month')) if request.form.get('month') != '' else None
        
        # Загружаем данные
        df_opinion = load_data_opinions(year, month)
        df_categories = load_data_categories(year, month)


        try:
            save_plot_to_html(lambda: plot_opinions(df_opinion), 'opinions.html')
            save_plot_to_html(lambda: plot_categories(df_categories), 'categories.html')
            
        except Exception as e:
            logger.error(f"Ошибка при построении графиков: {e}")
            return render_template(
                'index.html',
                message=f'Не удалось построить графики. Проверьте введенные данные.'
            )
        
        return render_template(
            'index.html',
            message=f'Графики за {"год" if year else ""}{f"{year} " if year else ""}{"месяц" if month else ""}{f"{month} " if month else ""}построены.',
            opinions_url='/opinions',
            categories_url='/categories',
        )
    else:
        return render_template('index.html')
    
@app.route('/opinions')
def show_opinions():
    return render_template('opinions.html')

@app.route('/categories')
def show_categories():
    return render_template('categories.html')

def create_app():
    return app

if __name__ == '__main__':
    app.run(debug=True)