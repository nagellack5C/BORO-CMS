from peewee import *

db = PostgresqlDatabase(
    'postgres',  # Required by Peewee.
    user='aklimov',  # Will be passed directly to psycopg2.
    # password='password',  # Ditto.
    host='localhost',  # Ditto.
    port=5432
)


class News(Model):
    date = DateField()
    text = TextField()
    images = TextField(null=True)

    class Meta:
        database = db


def add_news(date, text, images):
    News.insert(date=date, text=text, images=images).execute()


def get_next_10_news(offset=0):
    news = [item for item in News.select().offset(offset).limit(10).execute()]
    return [{'date': new.date, 'text': new.text, 'images': new.images} for new in news]


def init_db():
    db.drop_tables([News])
    db.create_tables([News])


if __name__ == '__main__':
    init_db()
