import unittest
from update_client import updateclient
import datetime


def validate_date_format(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")


class MyTestCase(unittest.TestCase):
    client = updateclient("John Doe, 999999999, 1960-01-01")

    def test_name_datatype(self):
        full_name = self.client.entry_fullname.get()
        name_split = full_name.split(", ")
        name = name_split[0]
        self.assertFalse(name.isnumeric())

    def test_SIN_length(self):
        full_name = self.client.entry_fullname.get()
        name_split = full_name.split(", ")
        sin = name_split[1]
        self.assertEqual(9, len(sin))

    def test_phone_datatype(self):
        phone_number = self.client.entry_phonenumber.get()
        self.assertTrue(phone_number.isnumeric())

    def test_phone_length(self):
        phone_number = self.client.entry_phonenumber.get()
        self.assertEqual(10, len(phone_number))

    def test_business_phone_datatype(self):
        business_phone_number = self.client.entry_buisnessphonenumber.get()
        self.assertTrue(business_phone_number.isnumeric())

    def test_business_phone_length(self):
        business_phone_number = self.client.entry_buisnessphonenumber.get()
        self.assertEqual(10, len(business_phone_number))

    def test_net_worth_datatype(self):
        net_worth = self.client.entry_networth.get()
        self.assertTrue(net_worth.isnumeric())

    def test_expenses_datatype(self):
        expenses = self.client.entry_expenses.get()
        self.assertTrue(expenses.isnumeric())

    def test_email(self):
        email = self.client.entry_email.get()
        self.assertEqual(True, email.__contains__("@"))

    def test_date_of_birth_format(self):
        full_name = self.client.entry_fullname.get()
        name_split = full_name.split(", ")
        date_of_birth = name_split[2]
        validate_date_format(date_of_birth)


if __name__ == '__main__':
    unittest.main()
