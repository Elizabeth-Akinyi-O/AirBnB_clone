#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_no_args(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        b_m1 = BaseModel()
        b_m2 = BaseModel()
        self.assertNotEqual(b_m1.id, b_m2.id)

    def test_two_models_different_created_at(self):
        b_m1 = BaseModel()
        sleep(0.05)
        b_m2 = BaseModel()
        self.assertLess(b_m1.created_at, b_m2.created_at)

    def test_two_models_different_updated_at(self):
        b_m1 = BaseModel()
        sleep(0.05)
        b_m2 = BaseModel()
        self.assertLess(b_m1.updated_at, b_m2.updated_at)

    def test_str_representation(self):
        da_ti = datetime.today()
        da_ti_repr = repr(da_ti)
        b_m = BaseModel()
        b_m.id = "123456"
        b_m.created_at = b_m.updated_at = da_ti
        b_mstr = b_m.__str__()
        self.assertIn("[BaseModel] (123456)", b_mstr)
        self.assertIn("'id': '123456'", b_mstr)
        self.assertIn("'created_at': " + da_ti_repr, b_mstr)
        self.assertIn("'updated_at': " + da_ti_repr, b_mstr)

    def test_args_unused(self):
        b_m = BaseModel(None)
        self.assertNotIn(None, b_m.__dict__.values())

    def test_instantiation_with_kwargs(self):
        da_ti = datetime.today()
        da_ti_iso = da_ti.isoformat()
        b_m = BaseModel(id="345", created_at=da_ti_iso, updated_at=da_ti_iso)
        self.assertEqual(b_m.id, "345")
        self.assertEqual(b_m.created_at, da_ti)
        self.assertEqual(b_m.updated_at, da_ti)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        da_ti = datetime.today()
        da_ti_iso = da_ti.isoformat()
        b_m = BaseModel("12", id="345", created_at=da_ti_iso, updated_at=da_ti_iso)
        self.assertEqual(b_m.id, "345")
        self.assertEqual(b_m.created_at, da_ti)
        self.assertEqual(b_m.updated_at, da_ti)


class TestBaseModel_save(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

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

    def test_one_save(self):
        b_m = BaseModel()
        sleep(0.05)
        first_updated_at = b_m.updated_at
        b_m.save()
        self.assertLess(first_updated_at, b_m.updated_at)

    def test_two_saves(self):
        b_m = BaseModel()
        sleep(0.05)
        first_updated_at = b_m.updated_at
        b_m.save()
        second_updated_at = b_m.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        b_m.save()
        self.assertLess(second_updated_at, b_m.updated_at)

    def test_save_with_arg(self):
        b_m = BaseModel()
        with self.assertRaises(TypeError):
            b_m.save(None)

    def test_save_updates_file(self):
        b_m = BaseModel()
        b_m.save()
        b_mid = "BaseModel." + b_m.id
        with open("file.json", "r") as f:
            self.assertIn(b_mid, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        b_m = BaseModel()
        self.assertTrue(dict, type(b_m.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        b_m = BaseModel()
        self.assertIn("id", b_m.to_dict())
        self.assertIn("created_at", b_m.to_dict())
        self.assertIn("updated_at", b_m.to_dict())
        self.assertIn("__class__", b_m.to_dict())

    def test_to_dict_contains_added_attributes(self):
        b_m = BaseModel()
        b_m.name = "Holberton"
        b_m.my_number = 98
        self.assertIn("name", b_m.to_dict())
        self.assertIn("my_number", b_m.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        b_m = BaseModel()
        b_m_dict = b_m.to_dict()
        self.assertEqual(str, type(b_m_dict["created_at"]))
        self.assertEqual(str, type(b_m_dict["updated_at"]))

    def test_to_dict_output(self):
        da_ti = datetime.today()
        b_m = BaseModel()
        b_m.id = "123456"
        b_m.created_at = b_m.updated_at = da_ti
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': da_ti.isoformat(),
            'updated_at': da_ti.isoformat()
        }
        self.assertDictEqual(b_m.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        b_m = BaseModel()
        self.assertNotEqual(b_m.to_dict(), b_m.__dict__)

    def test_to_dict_with_arg(self):
        b_m = BaseModel()
        with self.assertRaises(TypeError):
            b_m.to_dict(None)


if __name__ == "__main__":
    unittest.main()
