#!/usr/bin/python3
"""__init__ for models directory.
    Creates a FileStorage instance
"""


from models.engine.file_storage import FileStorage
storage = FileStorage()
storage.reload()
