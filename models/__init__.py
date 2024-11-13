#!/usr/bin/python3

import os

storage_type = os.environ.get('HBNB_TYPE_STORAGE', 'file')
db = os.environ.get('HBNB_ENV', 'test')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage as Storage
else:
    from models.engine.file_storage import FileStorage as Storage

storage = Storage()
storage.reload()

