#!/usr/bin/python3
"""test file storage"""


import unittest
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """test file storage"""

    @classmethod
    def setUpClass(cls):
        """set up for test"""
        cls.user = User()
        cls.user.first_name = "Khireddine"
        cls.user.last_name = "Khiro"
        cls.user.email = "34KK@gmail.com"
        cls.storage = FileStorage()

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        del cls.user

    def tearDown(self):
        """teardown"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_all(self):
        """tests if all works in File Storage"""
        storage = FileStorage()
        obj = storage.all()
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, storage._FileStorage__objects)

    def test_new(self):
        """test when new is created"""
        storage = FileStorage()
        obj = storage.all()
        user = User()
        user.id = 123455
        user.name = "Aiko"
        storage.new(user)
        key = user.__class__.__name__ + "." + str(user.id)
        self.assertIsNotNone(obj[key])

    def test_reload_filestorage(self):
        """
        tests reload
        """
        self.storage.save()
        Root = os.path.dirname(os.path.abspath("console.py"))
        path = os.path.join(Root, "file.json")
        with open(path, 'r') as f:
            lines = f.readlines()
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
        self.storage.save()
        with open(path, 'r') as f:
            lines2 = f.readlines()
        self.assertEqual(lines, lines2)
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
        with open(path, "w") as f:
            f.write("{}")
        with open(path, "r") as r:
            for line in r:
                self.assertEqual(line, "{}")
        self.assertIs(self.storage.reload(), None)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "not testing file storage")
    def test_get(self):
        """test the get method"""
        storage = FileStorage()
        self.assertIs(storage.get(User, "domain"), None)
        self.assertIs(storage.get("domain", "domain"), None)
        new_user = User()
        new_user.save()
        self.assertIs(storage.get(User, new_user.id), new_user)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == 'db',
                     "not testing file storage")
    def test_count(self):
        """test count method"""
        storage = FileStorage()
        initial_length = len(storage.all())
        self.assertEqual(storage.count(), initial_length)
        state_len = len(storage.all(State))
        self.assertEqual(storage.count(State), state_len)
        new_state = State()
        new_state.save()
        self.assertEqual(storage.count(), initial_length + 1)
        self.assertEqual(storage.count(State), state_len + 1)


if __name__ == "__main__":
    unittest.main()
