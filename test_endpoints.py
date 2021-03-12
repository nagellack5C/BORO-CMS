from main import app
from db import add_news, init_db


@app.route('/add_test_news', methods=['GET'])
def add_test_news():
    for i in range(1, 11):
        add_news(
            f'2010-10-{i}',
            'Тестовая новость!'#,
            # 'https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg'
        )
    return "OK!"


@app.route('/reinit_db', methods=['GET'])
def reinit_db():
    init_db()
    return "OK!"
