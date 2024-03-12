class TestHBNBCommand_prompt(unittest.TestCase):
    """Unittests for testing prompting of the HBNB command interpreter."""

    def test_prompt_string(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_emptyLine(self):
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", val.getvalue().strip())


class TestHBNBCommand_help(unittest.TestCase):
    """Unittests for testing help messages of the HBNB command interpreter.
        h_com = help command
    """

    def test_help_quit(self):
        h_com = "Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(h_com, val.getvalue().strip())

    def test_help_create(self):
        h_com = ("Usage: create <class>\n"
                 "Create a new class instance and print its id.")
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(h_com, val.getvalue().strip())

    def test_help_EOF(self):
        h_com = "EOF signal to exit the program."
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(h_com, val.getvalue().strip())

    def test_help_show(self):
        h_com = ("Usage: show <class> <id> or <class>.show(<id>)\n        "
                 "Display the string representation of a class instance of"
                 " a given id.")
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(h_com, val.getvalue().strip())

    def test_help_destroy(self):
        h_com = ("Usage: destroy <class> <id> or <class>.destroy(<id>)\n        "
                 "Delete a class instance of a given id.")
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(h_com, val.getvalue().strip())

    def test_help_all(self):
        h_com = ("Usage: all or all <class> or <class>.all()\n        "
                 "Display string representations of all instances of a given class"
                 ".\n        If no class is specified, displays all instantiated "
                 "objects.")
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(h_com, val.getvalue().strip())

    def test_help_count(self):
        h_com = ("Usage: count <class> or <class>.count()\n        "
                 "Retrieve the number of instances of a given class.")
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(h_com, val.getvalue().strip())

    def test_help_update(self):
        h_com = ("Usage: update <class> <id> <attribute_name> <attribute_value> or"
                 "\n       <class>.update(<id>, <attribute_name>, <attribute_value"
                 ">) or\n       <class>.update(<id>, <dictionary>)\n        "
                 "Update a class instance of a given id by adding or updating\n   "
                 "     a given attribute key/value pair or dictionary.")
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(h_com, val.getvalue().strip())

    def test_help(self):
        h_com = ("Documented commands (type help <topic>):\n"
                 "========================================\n"
                 "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(h_com, val.getvalue().strip())


class TestHBNBCommand_exit(unittest.TestCase):
    """Unittests for testing exiting from the HBNB command interpreter."""

    def test_quit_exits(self):
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommand_create(unittest.TestCase):
    """Unittests for testing create from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        Filestorage.__objects = {}

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

    def test_create_missing_class(self):
        output = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(output, val.getvalue().strip())

    def test_create_invalid_class(self):
        output = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(output, val.getvalue().strip())

    def test_create_invalid_syntax(self):
        output = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(output, val.getvalue().strip())
        output = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(output, val.getvalue().strip())

    def test_create_object(self):
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(val.getvalue().strip()))
            testKey = "BaseModel.{}".format(val.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(val.getvalue().strip()))
            testKey = "User.{}".format(val.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(val.getvalue().strip()))
            testKey = "State.{}".format(val.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(val.getvalue().strip()))
            testKey = "City.{}".format(val.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(val.getvalue().strip()))
            testKey = "Amenity.{}".format(val.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(val.getvalue().strip()))
            testKey = "Place.{}".format(val.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(val.getvalue().strip()))
            testKey = "Review.{}".format(val.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())


class TestHBNBCommand_show(unittest.TestCase):
    """Unittests for testing show from the HBNB command interpreter"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        Filestorage.__objects = {}

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

    def test_show_missing_class(self):
        output = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(output, val.getvalue().strip())

    def test_show_invalid_class(self):
        output = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            self.assertEqual(output, val.getvalue().strip())

    def test_show_missing_id_space_notation(self):
        output = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(output, val.getvalue().strip())

    def test_show_missing_id_dot_notation(self):
        output = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertEqual(output, val.getvalue().strip())

    def test_show_no_instance_found_space_notation(self):
        output = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("show User 1"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("show State 1"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("show City 1"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("show Place 1"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("show Review 1"))
            self.assertEqual(output, val.getvalue().strip())

    def test_show_no_instance_found_dot_notation(self):
        output = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(1)"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("User.show(1)"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("State.show(1)"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("City.show(1)"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show(1)"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Place.show(1)"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Review.show(1)"))
            self.assertEqual(output, val.getvalue().strip())

    def test_show_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["BaseModel.{}".format(test_id)]
            command = "show BaseModel {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["User.{}".format(test_id)]
            command = "show User {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["State.{}".format(test_id)]
            command = "show State {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["Place.{}".format(test_id)]
            command = "show Place {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["City.{}".format(test_id)]
            command = "show City {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["Amenity.{}".format(test_id)]
            command = "show Amenity {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["Review.{}".format(test_id)]
            command = "show Review {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), val.getvalue().strip())

    def test_show_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["BaseModel.{}".format(test_id)]
            command = "BaseModel.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["User.{}".format(test_id)]
            command = "User.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["State.{}".format(test_id)]
            command = "State.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["Place.{}".format(test_id)]
            command = "Place.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["City.{}".format(test_id)]
            command = "City.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["Amenity.{}".format(test_id)]
            command = "Amenity.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["Review.{}".format(test_id)]
            command = "Review.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), val.getvalue().strip())


class TestHBNBCommand_destroy(unittest.TestCase):
    """Unittests for testing destroy from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        Filestorage.__objects = {}

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
        storage.reload()

    def test_destroy_missing_class(self):
        output = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd(".destroy()"))
            self.assertEqual(output, val.getvalue().strip())

    def test_destroy_invalid_class(self):
        output = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
            self.assertEqual(output, val.getvalue().strip())

    def test_destroy_id_missing_space_notation(self):
        output = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("destroy User"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("destroy State"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("destroy City"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("destroy Place"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("destroy Review"))
            self.assertEqual(output, val.getvalue().strip())

    def test_destroy_id_missing_dot_notation(self):
        output = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("User.destroy()"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("State.destroy()"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("City.destroy()"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
            self.assertEqual(output, val.getvalue().strip())

    def test_destroy_invalid_id_space_notation(self):
        output = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("destroy User 1"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("destroy State 1"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("destroy City 1"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity 1"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("destroy Place 1"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("destroy Review 1"))
            self.assertEqual(output, val.getvalue().strip())

    def test_destroy_invalid_id_dot_notation(self):
        output = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(1)"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("User.destroy(1)"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("State.destroy(1)"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("City.destroy(1)"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy(1)"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy(1)"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy(1)"))
            self.assertEqual(output, val.getvalue().strip())


    def test_destroy_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["BaseModel.{}".format(test_id)]
            command = "destroy BaseModel {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["User.{}".format(test_id)]
            command = "show User {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["State.{}".format(test_id)]
            command = "show State {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["Place.{}".format(test_id)]
            command = "show Place {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["City.{}".format(test_id)]
            command = "show City {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["Amenity.{}".format(test_id)]
            command = "show Amenity {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["Review.{}".format(test_id)]
            command = "show Review {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())

    def test_destroy_objects_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["BaseModel.{}".format(test_id)]
            command = "BaseModel.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["User.{}".format(test_id)]
            command = "User.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["State.{}".format(test_id)]
            command = "State.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["Place.{}".format(test_id)]
            command = "Place.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["City.{}".format(test_id)]
            command = "City.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["Amenity.{}".format(test_id)]
            command = "Amenity.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            obj = storage.all()["Review.{}".format(test_id)]
            command = "Review.destory({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())


class TestHBNBCommand_all(unittest.TestCase):
    """Unittests for testing all of the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        Filestorage.__objects = {}

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

    def test_all_invalid_class(self):
        output = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("all MyModel"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
            self.assertEqual(output, val.getvalue().strip())

    def test_all_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("BaseModel", val.getvalue().strip())
            self.assertIn("User", val.getvalue().strip())
            self.assertIn("State", val.getvalue().strip())
            self.assertIn("Place", val.getvalue().strip())
            self.assertIn("City", val.getvalue().strip())
            self.assertIn("Amenity", val.getvalue().strip())
            self.assertIn("Review", val.getvalue().strip())

    def test_all_objects_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd(".all()"))
            self.assertIn("BaseModel", val.getvalue().strip())
            self.assertIn("User", val.getvalue().strip())
            self.assertIn("State", val.getvalue().strip())
            self.assertIn("Place", val.getvalue().strip())
            self.assertIn("City", val.getvalue().strip())
            self.assertIn("Amenity", val.getvalue().strip())
            self.assertIn("Review", val.getvalue().strip())

    def test_all_single_object_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", val.getvalue().strip())
            self.assertNotIn("User", val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("all User"))
            self.assertIn("User", val.getvalue().strip())
            self.assertNotIn("BaseModel", val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("all State"))
            self.assertIn("State", val.getvalue().strip())
            self.assertNotIn("BaseModel", val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("all City"))
            self.assertIn("City", val.getvalue().strip())
            self.assertNotIn("BaseModel", val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", val.getvalue().strip())
            self.assertNotIn("BaseModel", val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("all Place"))
            self.assertIn("Place", val.getvalue().strip())
            self.assertNotIn("BaseModel", val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("all Review"))
            self.assertIn("Review", val.getvalue().strip())
            self.assertNotIn("BaseModel", val.getvalue().strip())

    def test_all_single_object_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", val.getvalue().strip())
            self.assertNotIn("User", val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("User.all()"))
            self.assertIn("User", val.getvalue().strip())
            self.assertNotIn("BaseModel", val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("State.all()"))
            self.assertIn("State", val.getvalue().strip())
            self.assertNotIn("BaseModel", val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("City.all()"))
            self.assertIn("City", val.getvalue().strip())
            self.assertNotIn("BaseModel", val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            self.assertIn("Amenity", val.getvalue().strip())
            self.assertNotIn("BaseModel", val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Place.all()"))
            self.assertIn("Place", val.getvalue().strip())
            self.assertNotIn("BaseModel", val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Review.all()"))
            self.assertIn("Review", val.getvalue().strip())
            self.assertNotIn("BaseModel", val.getvalue().strip())


class TestHBNBCommand_update(unittest.TestCase):
    """Unittests for testing update from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        Filestorage.__objects = {}

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

    def test_update_missing_class(self):
        output = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            self.assertEqual(output, val.getvalue().strip())

    def test_update_invalid_class(self):
        output = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("update MyModel"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
            self.assertEqual(output, val.getvalue().strip())

    def test_update_missing_id_space_notation(self):
        output = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("update User"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("update State"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("update City"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("update Amenity"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("update Place"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("update Review"))
            self.assertEqual(output, val.getvalue().strip())

    def test_update_missing_id_dot_notation(self):
        output = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("User.update()"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("State.update()"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("City.update()"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Place.update()"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Review.update()"))
            self.assertEqual(output, val.getvalue().strip())

    def test_update_invalid_id_space_notation(self):
        output = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel 1"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("update User 1"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("update State 1"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("update City 1"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("update Amenity 1"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("update Place 1"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("update Review 1"))
            self.assertEqual(output, val.getvalue().strip())

    def test_update_invalid_id_dot_notation(self):
        output = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update(1)"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("User.update(1)"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("State.update(1)"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("City.update(1)"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update(1)"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Place.update(1)"))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Review.update(1)"))
            self.assertEqual(output, val.getvalue().strip())

    def test_update_missing_attr_name_space_notation(self):
        output = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = val.getvalue().strip()
            command = "update BaseModel {}".format(test_id)
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = val.getvalue().strip()
            command = "update User {}".format(test_id)
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = val.getvalue().strip()
            command = "update State {}".format(test_id)
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = val.getvalue().strip()
            command = "update City {}".format(test_id)
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = val.getvalue().strip()
            command = "update Amenity {}".format(test_id)
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = val.getvalue().strip()
            command = "update Place {}".format(test_id)
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())

    def test_update_missing_attr_name_dot_notation(self):
        output = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = val.getvalue().strip()
            command = "BaseModel.update({})".format(test_id)
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = val.getvalue().strip()
            command = "User.update({})".format(test_id)
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = val.getvalue().strip()
            command = "State.update({})".format(test_id)
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = val.getvalue().strip()
            command = "City.update({})".format(test_id)
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = val.getvalue().strip()
            command = "Amenity.update({})".format(test_id)
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = val.getvalue().strip()
            command = "Place.update({})".format(test_id)
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())

    def test_update_missing_attr_value_space_notation(self):
        output = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create BaseModel")
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            command = "update BaseModel {} attr_name".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create User")
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            command = "update User {} attr_name".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create State")
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            command = "update State {} attr_name".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create City")
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            command = "update City {} attr_name".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Amenity")
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            command = "update Amenity {} attr_name".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Place")
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            command = "update Place {} attr_name".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Review")
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            command = "update Review {} attr_name".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())

    def test_update_missing_attr_value_dot_notation(self):
        output = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create BaseModel")
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            command = "BaseModel.update({}, attr_name)".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create User")
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            command = "User.update({}, attr_name)".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create State")
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            command = "State.update({}, attr_name)".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create City")
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            command = "City.update({}, attr_name)".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Amenity")
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            command = "Amenity.update({}, attr_name)".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Place")
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            command = "Place.update({}, attr_name)".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Review")
            test_id = val.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as val:
            command = "Review.update({}, attr_name)".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(output, val.getvalue().strip())

    def test_update_valid_string_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create BaseModel")
            test_id = val.getvalue().strip()
        command = "update BaseModel {} attr_name 'attr_value'".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["BaseModel.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create User")
            test_id = val.getvalue().strip()
        command = "update User {} attr_name 'attr_value'".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["User.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create State")
            test_id = val.getvalue().strip()
        command = "update State {} attr_name 'attr_value'".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["State.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create City")
            test_id = val.getvalue().strip()
        command = "update City {} attr_name 'attr_value'".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["City.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Place")
            test_id = val.getvalue().strip()
        command = "update Place {} attr_name 'attr_value'".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Amenity")
            test_id = val.getvalue().strip()
        command = "update Amenity {} attr_name 'attr_value'".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["Amenity.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Review")
            test_id = val.getvalue().strip()
        command = "update Review {} attr_name 'attr_value'".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["Review.{}".format(test_id)].__dict__
        self.assertTrue("attr_value", test_dict["attr_name"])

    def test_update_valid_string_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create BaseModel")
            tId = val.getvalue().strip()
        command = "BaseModel.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["BaseModel.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create User")
            tId = val.getvalue().strip()
        command = "User.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["User.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create State")
            tId = val.getvalue().strip()
        command = "State.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["State.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create City")
            tId = val.getvalue().strip()
        command = "City.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["City.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Place")
            tId = val.getvalue().strip()
        command = "Place.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Amenity")
            tId = val.getvalue().strip()
        command = "Amenity.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["Amenity.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Review")
            tId = val.getvalue().strip()
        command = "Review.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["Review.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_int_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Place")
            test_id = val.getvalue().strip()
        command = "update Place {} max_guest 98".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_int_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Place")
            tId = val.getvalue().strip()
        command = "Place.update({}, max_guest, 98)".format(tId)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_float_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Place")
            test_id = val.getvalue().strip()
        command = "update Place {} latitude 7.2".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual(7.2, test_dict["latitude"])

    def test_update_valid_float_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Place")
            tId = val.getvalue().strip()
        command = "Place.update({}, latitude, 7.2)".format(tId)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual(7.2, test_dict["latitude"])

    def test_update_valid_dictionary_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create BaseModel")
            test_id = val.getvalue().strip()
        command = "update BaseModel {} ".format(test_id)
        command += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(command)
        test_dict = storage.all()["BaseModel.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create User")
            test_id = val.getvalue().strip()
        command = "update User {} ".format(test_id)
        command += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(command)
        test_dict = storage.all()["User.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create State")
            test_id = val.getvalue().strip()
        command = "update State {} ".format(test_id)
        command += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(command)
        test_dict = storage.all()["State.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create City")
            test_id = val.getvalue().strip()
        command = "update City {} ".format(test_id)
        command += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(command)
        test_dict = storage.all()["City.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Place")
            test_id = val.getvalue().strip()
        command = "update Place {} ".format(test_id)
        command += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(command)
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Amenity")
            test_id = val.getvalue().strip()
        command = "update Amenity {} ".format(test_id)
        command += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(command)
        test_dict = storage.all()["Amenity.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Review")
            test_id = val.getvalue().strip()
        command = "update Review {} ".format(test_id)
        command += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(command)
        test_dict = storage.all()["Review.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_dictionary_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create BaseModel")
            test_id = val.getvalue().strip()
        command = "BaseModel.update({}".format(test_id)
        command += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(command)
        test_dict = storage.all()["BaseModel.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create User")
            test_id = val.getvalue().strip()
        command = "User.update({}, ".format(test_id)
        command += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(command)
        test_dict = storage.all()["User.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create State")
            test_id = val.getvalue().strip()
        command = "State.update({}, ".format(test_id)
        command += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(command)
        test_dict = storage.all()["State.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create City")
            test_id = val.getvalue().strip()
        command = "City.update({}, ".format(test_id)
        command += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(command)
        test_dict = storage.all()["City.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Place")
            test_id = val.getvalue().strip()
        command = "Place.update({}, ".format(test_id)
        command += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(command)
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Amenity")
            test_id = val.getvalue().strip()
        command = "Amenity.update({}, ".format(test_id)
        command += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(command)
        test_dict = storage.all()["Amenity.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Review")
            test_id = val.getvalue().strip()
        command = "Review.update({}, ".format(test_id)
        command += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(command)
        test_dict = storage.all()["Review.{}".format(test_id)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_dictionary_with_int_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Place")
            test_id = val.getvalue().strip()
        command = "update Place {} ".format(test_id)
        command += "{'max_guest': 98})"
        HBNBCommand().onecmd(command)
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_dictionary_with_int_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Place")
            test_id = val.getvalue().strip()
        command = "Place.update({}, ".format(test_id)
        command += "{'max_guest': 98})"
        HBNBCommand().onecmd(command)
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_dictionary_with_float_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Place")
            test_id = val.getvalue().strip()
        command = "update Place {} ".format(test_id)
        command += "{'latitude': 9.8})"
        HBNBCommand().onecmd(command)
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual(9.8, test_dict["latitude"])

    def test_update_valid_dictionary_with_float_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as val:
            HBNBCommand().onecmd("create Place")
            test_id = val.getvalue().strip()
        command = "Place.update({}, ".format(test_id)
        command += "{'latitude': 9.8})"
        HBNBCommand().onecmd(command)
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual(9.8, test_dict["latitude"])


class TestHBNBCommand_count(unittest.TestCase):
    """Unittests for testing count method of HBNB comand interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        Filestorage._Filestorage__objects = {}

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

    def test_count_invalid_class(self):
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
            self.assertEqual("0", val.getvalue().strip())

    def test_count_object(self):
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
            self.assertEqual("1", val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("User.count()"))
            self.assertEqual("1", val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("State.count()"))
            self.assertEqual("1", val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Place.count()"))
            self.assertEqual("1", val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("City.count()"))
            self.assertEqual("1", val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
            self.assertEqual("1", val.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as val:
            self.assertFalse(HBNBCommand().onecmd("Review.count()"))
            self.assertEqual("1", val.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
