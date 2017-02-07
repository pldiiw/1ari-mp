import unittest
from random import seed
from string import ascii_uppercase

from JeffersonShell import (
    generate_cylinder, generate_key, is_key_valid, load_cylinders_from_file,
    sanitize_message, write_cylinders_to_file, find, shift, jefferson_shift)


class JeffersonShellTests(unittest.TestCase):
    def test_sanitize_message(self):
        one = "Welcome"
        one_should = "Welcome"
        self.assertEqual(sanitize_message(one), one_should)

        two = "Welcome to my House"
        two_should = "WelcometomyHouse"
        self.assertEqual(sanitize_message(two), two_should)

        three = "Weé_l-ç^(c)'ôom ?!!:§$ e."
        three_should = "Welcome"
        self.assertEqual(sanitize_message(three), three_should)

    def test_generate_cylinder(self):
        seed(5)
        one = generate_cylinder()
        one_should = 'TIXLUQAOHBFVPRDGYSWZNJMEKC'
        self.assertEqual(one, one_should)
        self.assertEqual(''.join(sorted(one)), ascii_uppercase)

        two = generate_cylinder()
        two_should = 'FYCETVOWSAQDMUXLRZNJIBGKPH'
        self.assertEqual(two, two_should)
        self.assertEqual(''.join(sorted(two)), ascii_uppercase)

        seed(55)
        three = generate_cylinder()
        three_should = 'CGEJZFWVLPMYIOUQNAXTBHKSRD'
        self.assertEqual(three, three_should)
        self.assertEqual(''.join(sorted(three)), ascii_uppercase)

    def test_load_cylinders_from_file(self):
        file = 'cylinders_test.txt'
        seed(10)
        write_cylinders_to_file(file, 5)
        seed(10)
        should = {
            1: generate_cylinder(),
            2: generate_cylinder(),
            3: generate_cylinder(),
            4: generate_cylinder(),
            5: generate_cylinder()
        }
        self.assertEqual(load_cylinders_from_file(file), should)

    def is_key_valid(self):
        one = [2, 4, 1, 8, 3, 5, 7, 6]
        self.assertTrue(is_key_valid(one, 8))

        two = [2, 5, 4, 3]
        self.assertFalse(is_key_valid(two, 5))

    def test_generate_key(self):
        seed(2)
        one = generate_key(20)
        one_should = [
            2, 3, 19, 12, 6, 17, 13, 11, 5, 15, 10, 4, 1, 14, 16, 20, 9, 18, 7,
            8
        ]
        self.assertEqual(one, one_should)

        seed(13)
        two = generate_key(10)
        two_should = [5, 10, 3, 6, 2, 7, 9, 8, 1, 4]
        self.assertEqual(two, two_should)

    def test_find(self):
        one = find("l", "hello")
        one_should = 2
        self.assertEqual(one, one_should)

        two = find("x", "The fox jumped over the wall.")
        two_should = 6
        self.assertEqual(two, two_should)

    def test_shift(self):
        one = shift(12, 20, 5)
        one_should = 2
        self.assertEqual(one, one_should)

        two = shift(2, 42, 3)
        two_should = 2
        self.assertEqual(two, two_should)

    def test_jefferson_shift(self):
        one = jefferson_shift(4)
        one_should = 10
        self.assertEqual(one, one_should)

        two = jefferson_shift(25)
        two_should = 5
        self.assertEqual(two, two_should)

        three = jefferson_shift(43239)
        three_should = 7
        self.assertEqual(three, three_should)


if __name__ == "__main__":
    unittest.main()
