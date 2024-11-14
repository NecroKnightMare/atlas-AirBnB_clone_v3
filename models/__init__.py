#!/usr/bin/python3

from os import getenv

storage_type = getenv('HBNB_TYPE_STORAGE, file')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage as Storage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage as Storage
    storage = FileStorage()

storage = Storage()
storage.reload()
