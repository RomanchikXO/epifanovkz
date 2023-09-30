from peewee import *

db = SqliteDatabase("epifanovDB")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    """
    Описание пользователя
    """
    name = CharField()
    telegram_id = IntegerField()
    profession = CharField()


class Tasks(BaseModel):
    """
    Описание задачи

    Этот класс используется для хранения информации о задачах.
    Атрибуты:
    - name_patient (str): Имя пациента, для которого создана задача.
    - task (str): Описание самой задачи.
    - date (int): Дата выполнения задачи (может быть в формате Unix timestamp).
    - status (bool): Статус задачи. True, если задача выполнена, False, если не выполнена, None, если статус не определен.
    """
    name_patient = CharField()
    task = CharField()
    date = IntegerField()
    status = BooleanField(default=None)


def create_tables():
    db.connect()
    db.create_tables([User, Tasks], safe=True)
