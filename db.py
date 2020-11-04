import os
import io
from urllib.parse import urlparse
from PIL import Image
from peewee import *

# code to enable db usage on both Heroku and localhost.
if os.environ.get('DATABASE_URL'):
    DATABASE_URL = os.environ.get('DATABASE_URL')
    db = urlparse(DATABASE_URL)
    user = db.username
    password = db.password
    path = db.path[1:]
    host = db.hostname
    port = db.port
    db = PostgresqlDatabase(path, user=user, password=password, host=host, port=port)
else:
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

    class Meta:
        database = db


class Images(Model):
    """
    Stores binary images and thumbs.
    """
    name = CharField(60)
    folder = CharField(60)
    relation_id = IntegerField(null=True) # needed to get images for e.g. particular news items
    image = BlobField()
    thumb = BlobField(null=True)

    class Meta:
        database = db
        indexes = (
            (('name', 'folder'), True),
        )


def add_news(date, text):
    return News.insert(date=date, text=text).execute()


def get_news(offset, limit, id=None):
    """
    Get news from database.
    :param offset:
    :param limit:
    :param id: particular news id
    :return:
    """
    if id is not None: # return a particular news item fast; will use this for editing
        return [new for new in News.select().where(News.id == id).execute()][0]

    news = [item for item in
            News.select().order_by(News.id.desc()).offset(offset).limit(limit).execute()]

    def get_image_src_links(news_id):
        """
        Return all URLs for a particular news id.
        """
        folder = f'news/{news_id}'
        images = [f'images/{img.folder}/{img.name}' for img in Images.select(
            Images.name, Images.folder).where(
            Images.folder == folder
        ).execute()]
        return images

    return [{
        'date': new.date,
        'text': new.text,
        'img_links': get_image_src_links(new.id)
    } for new in news]


def get_image_from_db(folder, name, thumb=False):
    """
    Get a single image or its thumb from DB.
    :param folder: folder column (category + id)
    :param name: image name
    :param thumb: True if thumbnail is needed
    :return:
    """
    image = [i for i in Images.select().where(
        Images.folder == folder, Images.name == name
    ).execute()][0]
    if thumb:
        return image.thumb.tobytes()
    return image.image.tobytes()


def add_image(image_name, image_folder, image_bytes):
    """
    Add a single image and its thumbnail to the DB.
    :param image_name:
    :param image_folder:
    :param image_bytes: image as a bytes sequence.
    :return:
    """
    if len(image_name) > 60:
        image_name = image_name[-60:]
    img = Image.open(io.BytesIO(image_bytes))
    img.thumbnail((250, 250))
    thumb = io.BytesIO()
    img.save(thumb, format='PNG')
    thumb = thumb.getvalue()
    Images.insert(
        name=image_name,
        folder=image_folder,
        image=image_bytes,
        thumb=thumb
    ).execute()


def init_db():
    """
    Reinit the DB.
    :return:
    """
    db.drop_tables([News, Images])
    db.create_tables([News, Images])


if __name__ == '__main__':
    init_db()
    print('reinit!')
