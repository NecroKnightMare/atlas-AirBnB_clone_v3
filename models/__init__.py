#!/usr/bin/python3

from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
import os

storage_type = os.environ.get('HBNB_TYPE_STORAGE', 'file')
db = os.environ.get('HBNB_ENV', 'test')

if storage_type == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

# storage = Storage()
storage.reload()
