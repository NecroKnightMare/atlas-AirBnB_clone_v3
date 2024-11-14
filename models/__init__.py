#!/usr/bin/python3

from os import getenv
from models import storage

storage_type = getenv('HBNB_TYPE_STORAGE, file')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage as Storage
else:
    from models.engine.file_storage import FileStorage as Storage

# storage = Storage()
storage.reload()
