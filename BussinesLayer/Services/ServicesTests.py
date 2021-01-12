import unittest
from BussinesLayer.Services.Login import log_in
from BussinesLayer.Services.Register import registration
from BussinesLayer.Services.Logout import log_out
import random
import string
from BussinesLayer.Services.Logger import info


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


class ServicesTests(unittest.TestCase):
    info("--------------UNIT TESTS RUN: --------------")

    def test_success_login(self):
        self.assertEqual(log_in('orel', '123456'), "Successfully Login")

    def test_fail_login(self):
        self.assertEqual(log_in('or', 'or'), 'No user Found')

    def test_success_register(self):
        random_name = get_random_string(5)
        random_pass = get_random_string(5)
        self.assertEqual(registration('1111', '1111', '1111', '1111', random_name, random_pass), "Successfully Registration")

    def test_fail_exist_user_register(self):
        self.assertEqual(registration('1111', '1111', '1111', '1111', 'orel', '123456'), "username has exist")

    def test_fail_exist_user_and_pass_register(self):
        self.assertEqual(registration('1111', '1111', '1111', '1111', 'orel', '1234'), "username has exist")

    def test_empty_name_register(self):
        self.assertEqual(registration('', '1111', '1111', '1111', 'ore', '123456'),
                         "FAILED - empty field/short passwords")

    def test_empty_last_name_register(self):
        self.assertEqual(registration('1111', '', '1111', '1111', 'ore', '123456'),
                         "FAILED - empty field/short passwords")

    def test_empty_phone_register(self):
        self.assertEqual(registration('1111', '1111', '', '1111', 'ore', '123456'),
                         "FAILED - empty field/short passwords")

    def test_empty_name_register(self):
        self.assertEqual(registration('1111', '1111', '1111', '', 'ore', '123456'),
                         "FAILED - empty field/short passwords")

    def test_empty_username_register(self):
        self.assertEqual(registration('1111', '1111', '1111', '1111', '', '123456'),
                         "FAILED - empty field/short passwords")

    def test_empty_pass_register(self):
        self.assertEqual(registration('1111', '1111', '1111', '1111', 'orel', ''),
                         "FAILED - empty field/short passwords")

    def test_logout(self):
        self.assertEqual(log_out(), "bye bye")


if __name__ == '__main__':
    unittest.main()

