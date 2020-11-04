import os
from datetime import datetime
from flask import Flask, render_template, request, make_response, jsonify
from flask_bootstrap import Bootstrap
from db import get_news, add_news, add_image, get_image_from_db

app = Flask(__name__)
Bootstrap(app)

import test_endpoints

# export FLASK_APP=main.py
# export FLASK_ENV=development
# flask run


@app.route('/')
def news():
    """
    Render the main page with news.
    """
    return render_template('base.html', title='Главная страница', news=
                           get_news(0, 10), templates=["news.html"])


@app.route('/admin_news', methods=['GET', 'POST'])
def admin_news():
    """
    GET: render the admin page where the admin can add news.
    POST: read and parse news requests made on this page.
    """
    if request.method == 'GET':
        return render_template('admin_news.html')
    if request.method == 'POST':
        images = request.files.getlist('image')
        date = request.form['date']
        text = request.form['text']
        if not (date and text):
            return jsonify(success=False)
        news_id = add_news(date, text)
        if images:
            for image in images:
                add_image(image.filename.lower(), f'news/{news_id}', image.read())
        return jsonify(success=True)



@app.route('/images/<folder>/<item_id>/<image_name>')
@app.route('/images/<folder>/<item_id>/<image_name>/<option>')
def get_image(folder, item_id, image_name, option=False):
    """
    Get a single image from the database.
    :param folder: folder or category of the image
    :param item_id: id of e.g. news item
    :param image_name: name of image
    :param option: 'thumb' or 'full'
    """
    if image_name.lower().endswith(('.jpg', '.png')):
        thumb = False
        if option == 'thumb':
            thumb = True
        if option == 'full':
            return render_template('image.html', source_img=f'/images/{folder}/{item_id}/{image_name}')
        image_binary = get_image_from_db(f'{folder}/{item_id}', image_name, thumb=thumb)
        response = make_response(image_binary)
        response.headers.set('Content-Type', 'image/jpeg')
        filename = f'{folder}-{image_name}'
        if thumb:
            filename = f'thumb-{folder}-{image_name}'
        response.headers.set(
            'Content-Disposition', 'attachment', filename=filename)
        return response


@app.context_processor
def template_globals():
    """
    Define global vars to use in all templates.
    """
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
