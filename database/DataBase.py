from peewee import *

db = SqliteDatabase("epifanovDB")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    """
    Описание пользователя

    Этот класс используется для хранения информации о пользователях.
    Атрибуты:
    - name (str): Имя пользователя.
    - telegram_id (int): Идентификатор пользователя в Telegram.
    - profession (str): Профессия пользователя.
    """
    name = CharField()
    telegram_id = IntegerField()
    profession = CharField()


class Tasks(BaseModel):
    """
    Описание задачи

    Этот класс используется для хранения информации о задачах.
    Атрибуты:
    - doc (str): Специалист создающий задачу
    - name_patient (str): Имя пациента, для которого создана задача.
    - task (str): Описание самой задачи.
    - date (int): Дата выполнения задачи (может быть в формате Unix timestamp).
    - status (bool): Статус задачи. True, если задача выполнена, False, если не выполнена, None, если статус не определен.
    - comment_if_done (str): Комментарий к задаче, если она выполнена. По умолчанию None, если комментарий не указан.

    """
    doc = CharField(default=None, null=True)
    name_patient = CharField()
    task = CharField()
    date = CharField()
    status = BooleanField(default=None, null=True)
    comment_if_done = CharField(default=None, null=True)



def create_tables():
    db.connect()
    db.create_tables([User, Tasks], safe=True)
