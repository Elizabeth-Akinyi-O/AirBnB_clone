#!/usr/bin/python3
"""Defines unittests for models/review.py.

Unittest classes:
    TestReview_instantiation
    TestReview_save
    TestReview_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReview_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Review class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(self):
        rvw = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(rvw))
        self.assertNotIn("place_id", rvw.__dict__)

    def test_user_id_is_public_class_attribute(self):
        rvw = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(rvw))
        self.assertNotIn("user_id", rvw.__dict__)

    def test_text_is_public_class_attribute(self):
        rvw = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(rvw))
        self.assertNotIn("text", rvw.__dict__)

    def test_two_reviews_unique_ids(self):
        rvw1 = Review()
        rvw2 = Review()
        self.assertNotEqual(rvw1.id, rvw2.id)

    def test_two_reviews_different_created_at(self):
        rvw1 = Review()
        sleep(0.05)
        rvw2 = Review()
        self.assertLess(rvw1.created_at, rvw2.created_at)

    def test_two_reviews_different_updated_at(self):
        rvw1 = Review()
        sleep(0.05)
        rvw2 = Review()
        self.assertLess(rvw1.updated_at, rvw2.updated_at)

    def test_str_representation(self):
        da_ti = datetime.today()
        da_ti_repr = repr(da_ti)
        rvw = Review()
        rvw.id = "123456"
        rvw.created_at = rvw.updated_at = da_ti
        rvwstr = rvw.__str__()
        self.assertIn("[Review] (123456)", rvwstr)
        self.assertIn("'id': '123456'", rvwstr)
        self.assertIn("'created_at': " + da_ti_repr, rvwstr)
        self.assertIn("'updated_at': " + da_ti_repr, rvwstr)

    def test_args_unused(self):
        rvw = Review(None)
        self.assertNotIn(None, rvw.__dict__.values())

    def test_instantiation_with_kwargs(self):
        da_ti = datetime.today()
        da_ti_iso = da_ti.isoformat()
        rvw = Review(id="345", created_at=da_ti_iso, updated_at=da_ti_iso)
        self.assertEqual(rvw.id, "345")
        self.assertEqual(rvw.created_at, da_ti)
        self.assertEqual(rvw.updated_at, da_ti)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """Unittests for testing save method of the Review class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

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
        rvw = Review()
        sleep(0.05)
        first_updated_at = rvw.updated_at
        rvw.save()
        self.assertLess(first_updated_at, rvw.updated_at)

    def test_two_saves(self):
        rvw = Review()
        sleep(0.05)
        first_updated_at = rvw.updated_at
        rvw.save()
        second_updated_at = rvw.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        rvw.save()
        self.assertLess(second_updated_at, rvw.updated_at)

    def test_save_with_arg(self):
        rvw = Review()
        with self.assertRaises(TypeError):
            rvw.save(None)

    def test_save_updates_file(self):
        rvw = Review()
        rvw.save()
        rvwid = "Review." + rvw.id
        with open("file.json", "r") as f:
            self.assertIn(rvwid, f.read())


class TestReview_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Review class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        rvw = Review()
        self.assertIn("id", rvw.to_dict())
        self.assertIn("created_at", rvw.to_dict())
        self.assertIn("updated_at", rvw.to_dict())
        self.assertIn("__class__", rvw.to_dict())

    def test_to_dict_contains_added_attributes(self):
        rvw = Review()
        rvw.middle_name = "Holberton"
        rvw.my_number = 98
        self.assertEqual("Holberton", rvw.middle_name)
        self.assertIn("my_number", rvw.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        rvw = Review()
        rvw_dict = rvw.to_dict()
        self.assertEqual(str, type(rvw_dict["id"]))
        self.assertEqual(str, type(rvw_dict["created_at"]))
        self.assertEqual(str, type(rvw_dict["updated_at"]))

    def test_to_dict_output(self):
        da_ti = datetime.today()
        rvw = Review()
        rvw.id = "123456"
        rvw.created_at = rvw.updated_at = da_ti
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': da_ti.isoformat(),
            'updated_at': da_ti.isoformat(),
        }
        self.assertDictEqual(rvw.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        rvw = Review()
        self.assertNotEqual(rvw.to_dict(), rvw.__dict__)

    def test_to_dict_with_arg(self):
        rvw = Review()
        with self.assertRaises(TypeError):
            rvw.to_dict(None)


if __name__ == "__main__":
    unittest.main()
