import unittest
from os import remove
from random import seed
from string import ascii_uppercase

from JeffersonShell import (cipher_letter, cipher_message, find, generate_disk,
                            generate_key, is_key_valid, jefferson_shift,
                            load_cylinder_from_file, sanitize_message, shift,
                            write_cylinder_to_file)


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

    def test_generate_disk(self):
        seed(5)
        one = generate_disk()
        one_should = 'TIXLUQAOHBFVPRDGYSWZNJMEKC'
        self.assertEqual(one, one_should)
        self.assertEqual(''.join(sorted(one)), ascii_uppercase)

        two = generate_disk()
        two_should = 'FYCETVOWSAQDMUXLRZNJIBGKPH'
        self.assertEqual(two, two_should)
        self.assertEqual(''.join(sorted(two)), ascii_uppercase)

        seed(55)
        three = generate_disk()
        three_should = 'CGEJZFWVLPMYIOUQNAXTBHKSRD'
        self.assertEqual(three, three_should)
        self.assertEqual(''.join(sorted(three)), ascii_uppercase)

    def test_load_cylinder_from_file(self):
        file = 'cylinder_test.txt'
        seed(10)
        write_cylinder_to_file(file, 5)
        seed(10)
        should = {
            1: generate_disk(),
            2: generate_disk(),
            3: generate_disk(),
            4: generate_disk(),
            5: generate_disk()
        }
        self.assertEqual(load_cylinder_from_file(file), should)
        remove(file)

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

    def test_cipher_letter(self):
        one = cipher_letter("E", "YVOFUIRBJTMXQLZAWHCNEGKDSP")
        one_should = "Y"
        self.assertEqual(one, one_should)

        two = cipher_letter("A", "SUNIBHLAPVZYWOKEMCJXRDFTGQ")
        two_should = "O"
        self.assertEqual(two, two_should)

    def test_cipher_message(self):
        message_one = "ENJOY"
        cylinder_one = {
            1: "FEWPQLHBDSMCNAXIJTKUOZYVRG",
            2: "UGWAEIXHTOVRKSQBNJPCYFMDLZ",
            3: "BVWYUZKLGQXHJOTDSMNRIECPFA",
            4: "UJEDQRSHOCFBWANMITXPZYKVLG",
            5: "JBFULONATYWEHRPZVXSCKDIGQM"
        }
        key_one = [3, 2, 5, 1, 4]
        one = cipher_message(message_one, key_one, cylinder_one)
        one_should = "VMNFJ"
        self.assertEqual(one, one_should)


if __name__ == "__main__":
    unittest.main()
