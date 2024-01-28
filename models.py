from peewee import Model, CharField, AutoField
from database_manager import DatabaseManager
import local_settings

database_manager = DatabaseManager(
    database_name=local_settings.DATABASE["name"],
    user=local_settings.DATABASE["user"],
    password=local_settings.DATABASE["password"],
    host=local_settings.DATABASE["host"],
    port=local_settings.DATABASE["port"],
)


class Contact(Model):
    id = AutoField()
    first_name = CharField()
    last_name = CharField()
    phone_number = CharField()
    address = CharField()

    class Meta:
        database = database_manager.db


try:
    database_manager.create_tables(models=[Contact])
    print("Connect to DataBase Successfully!")
except Exception as error:
    print("Error", error)
finally:
    # closing database connection.
    if database_manager.db:
        database_manager.db.close()
