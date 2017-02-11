import unittest

from JeffersonGUI import (rotate_disk, rotate_disk_from_cylinder_in_place,
                          shift_list)


class JeffersonGUITests(unittest.TestCase):
    def test_shift_list(self):
        list_one = [1, 3, 10, 6, 2, 7, "abc", "def", 9, 8, "ghi"]
        one = shift_list(list_one, 5)
        one_should = ["abc", "def", 9, 8, "ghi", 1, 3, 10, 6, 2, 7]
        self.assertEqual(one, one_should)

        list_two = ["hello", [1, 2, 3], 100, 200, 300, "yo"]
        two = shift_list(list_two, -3)
        two_should = [200, 300, "yo", "hello", [1, 2, 3], 100]
        self.assertEqual(two, two_should)

    def test_rotate_disk(self):
        disk_one = "HQXRNLSJCMDUFWIPBVOEAZGTYK"
        one = rotate_disk(rotate_disk(disk_one, False), False)
        one_should = "YKHQXRNLSJCMDUFWIPBVOEAZGT"
        self.assertEqual(one, one_should)

        disk_two = "FRDKXIHMZPVQBJLACOYGTWNEUS"
        two = rotate_disk(disk_two)
        two_should = "RDKXIHMZPVQBJLACOYGTWNEUSF"
        self.assertEqual(two, two_should)

    def test_rotate_disk_from_cylinder_in_place(self):
        cylinder_one = {
            1: "BVWMXKQYSOCHTEAZRLUJDIFGPN",
            2: "YIQMOKUWAZHTDBRCLGJXVEFNPS"
        }
        rotate_disk_from_cylinder_in_place(cylinder_one, 1, False)
        rotate_disk_from_cylinder_in_place(cylinder_one, 1, False)
        rotate_disk_from_cylinder_in_place(cylinder_one, 2)
        cylinder_one_should = {
            1: "PNBVWMXKQYSOCHTEAZRLUJDIFG",
            2: "IQMOKUWAZHTDBRCLGJXVEFNPSY"
        }
        self.assertEqual(cylinder_one, cylinder_one_should)


if __name__ == "__main__":
    unittest.main()
