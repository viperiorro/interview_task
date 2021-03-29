from unittest import TestCase

from ddt import ddt, data, unpack

import handler


@ddt
class Test(TestCase):
    def test_successful_pass(self):
        event = {
            "FirstName": "Ivan",
            "LastName": "Ivanov",
            "Age": 18,
        }

        expected = {
            "FullName": "Ivan Ivanov",
            "AgeGroup": "Teenager",
        }
        result = handler.execute(event)
        self.assertDictEqual(result, expected)

    @data({}, [], 0, False, "", None)
    def test_no_first_name(self, value):
        event = {
            "FirstName": value,
            "LastName": "Ivanov",
            "Age": 18,
        }
        with self.assertRaises(handler.FirstNameNotFound):
            handler.execute(event)

    @data({}, [], 0, False, "", None)
    def test_no_last_name(self, value):
        event = {
            "FirstName": "Ivan",
            "LastName": value,
            "Age": 18,
        }
        with self.assertRaises(handler.LastNameNotFound):
            handler.execute(event)

    @data(["hello"], 1, True, False, 200, 3.14)
    def test_first_name_invalid_data_type(self, value):
        event = {
            "FirstName": value,
            "LastName": "Ivanov",
            "Age": 18,
        }
        with self.assertRaises(handler.InvalidParameterType):
            handler.execute(event)

    @data(["hello"], 1, True, False, 200, 3.14)
    def test_last_name_invalid_data_type(self, value):
        event = {
            "FirstName": "Ivan",
            "LastName": value,
            "Age": 18,
        }
        with self.assertRaises(handler.InvalidParameterType):
            handler.execute(event)

    @data("~!@#$%^&*().<>?\/'`[]-=+|", '"', "1Ivan1", "0Ivan0")
    def test_first_name_invalid_data(self, value):
        event = {
            "FirstName": value,
            "LastName": "Ivanov",
            "Age": 18,
        }
        with self.assertRaises(handler.InvalidParameterType):
            handler.execute(event)

    @data("~!@#$%^&*().<>?\/'`[]-=+|", '"', "1Ivan1", "0Ivan0", "Ivan\1", "Ivan\\1", "\nataly")
    def test_last_name_invalid_data(self, value):
        event = {
            "FirstName": "Ivan",
            "LastName": value,
            "Age": 18,
        }
        with self.assertRaises(handler.InvalidParameterPattern):
            handler.execute(event)

    @unpack
    @data(
        (0, "Unknown"),
        (1, "Child"),
        (10, "Child"),
        (11, "Teenager"),
        (19, "Teenager"),
        (20, "Adult"),
        (21, "Adult"),
    )
    def test_age_valid_data(self, age, age_group):
        event = {
            "FirstName": "Ivan",
            "LastName": "Ivanov",
            "Age": age,
        }
        expected = {
            "FullName": "Ivan Ivanov",
            "AgeGroup": age_group,
        }
        result = handler.execute(event)
        self.assertDictEqual(result, expected)

    @data([], {}, -1, "", "10", True, False, None)
    def test_age_invalid_data(self, age):
        event = {
            "FirstName": "Ivan",
            "LastName": "Ivanov",
            "Age": age,
        }
        with self.assertRaises(handler.InvalidParameterValue):
            handler.execute(event)
