from playhouse.migrate import *
import os


DB_NAME = file_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'epifanovDB'))


my_db = SqliteDatabase(DB_NAME)
migrator = SqliteMigrator(my_db)

with my_db.atomic():
    migrate(
        migrator.add_column('Tasks', 'doc', CharField(default=None, null=True)),
    )
