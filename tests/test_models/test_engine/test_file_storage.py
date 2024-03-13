#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.

Unittest classes:
    TestFileStorage_instantiation
    TestFileStorage_methods
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_FileStorage_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_objects_is_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        b_m = BaseModel()
        usr = User()
        st = State()
        plc = Place()
        cty = City()
        amty = Amenity()
        rvw = Review()
        models.storage.new(b_m)
        models.storage.new(usr)
        models.storage.new(st)
        models.storage.new(plc)
        models.storage.new(cty)
        models.storage.new(amty)
        models.storage.new(rvw)
        self.assertIn("BaseModel." + b_m.id, models.storage.all().keys())
        self.assertIn(b_m, models.storage.all().values())
        self.assertIn("User." + usr.id, models.storage.all().keys())
        self.assertIn(usr, models.storage.all().values())
        self.assertIn("State." + st.id, models.storage.all().keys())
        self.assertIn(st, models.storage.all().values())
        self.assertIn("Place." + plc.id, models.storage.all().keys())
        self.assertIn(plc, models.storage.all().values())
        self.assertIn("City." + cty.id, models.storage.all().keys())
        self.assertIn(cty, models.storage.all().values())
        self.assertIn("Amenity." + amty.id, models.storage.all().keys())
        self.assertIn(amty, models.storage.all().values())
        self.assertIn("Review." + rvw.id, models.storage.all().keys())
        self.assertIn(rvw, models.storage.all().values())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        b_m = BaseModel()
        usr = User()
        st = State()
        plc = Place()
        cty = City()
        amty = Amenity()
        rvw = Review()
        models.storage.new(b_m)
        models.storage.new(usr)
        models.storage.new(st)
        models.storage.new(plc)
        models.storage.new(cty)
        models.storage.new(amty)
        models.storage.new(rvw)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + b_m.id, save_text)
            self.assertIn("User." + usr.id, save_text)
            self.assertIn("State." + st.id, save_text)
            self.assertIn("Place." + plc.id, save_text)
            self.assertIn("City." + cty.id, save_text)
            self.assertIn("Amenity." + amty.id, save_text)
            self.assertIn("Review." + rvw.id, save_text)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        b_m = BaseModel()
        usr = User()
        st = State()
        plc = Place()
        cty = City()
        amty = Amenity()
        rvw = Review()
        models.storage.new(b_m)
        models.storage.new(usr)
        models.storage.new(st)
        models.storage.new(plc)
        models.storage.new(cty)
        models.storage.new(amty)
        models.storage.new(rvw)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + b_m.id, objs)
        self.assertIn("User." + usr.id, objs)
        self.assertIn("State." + st.id, objs)
        self.assertIn("Place." + plc.id, objs)
        self.assertIn("City." + cty.id, objs)
        self.assertIn("Amenity." + amty.id, objs)
        self.assertIn("Review." + rvw.id, objs)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
