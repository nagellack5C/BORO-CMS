import json
from datetime import datetime
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from db import get_next_10_news
app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def news():
    return render_template('news.html', title='Главная страница', news=
                           get_next_10_news(0))


@app.route('/admin_news', methods=['GET', 'POST'])
def admin_news():
    if request.method == 'GET':
        return render_template('admin_news.html')
    if request.method == 'POST':
        print([i for i in request.form.keys()])
        # print(request.form)
        return request.data


@app.context_processor
def template_globals():
    datenow = datetime.now()
    return dict(
        left_menu = {
            ('Сведения об образовательной организации', 'test.html'),
            ('Уставные документы учреждения', 'test.html'),
            ('Финансово-хозяйственная деятельность', 'test.html'),
            ('Школьные локальные акты', 'test.html'),
            ('Школьный управляющий совет', 'test.html'),
            ('Школа гражданского становления', 'test.html'),
            ('Информационная безопасность', 'test.html'),
            ('Воспитательная работа', 'test.html'),
            ('Питание учащихся', 'test.html'),
            ('Архив', 'test.html'),
            ('Летняя оздоровительная кампания', 'test.html')
        }, date=f'{datenow.day}.{datenow.month}.{datenow.year}',
        year=datenow.year
    )
